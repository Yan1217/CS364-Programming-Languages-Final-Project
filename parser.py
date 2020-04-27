from Lexer import Lexer
from ast import *
from typing import Sequence, Union, Optional

"""
  Program         →  { FunctionDef }
  FunctionDef     →  Type id ( Params ) { Declarations Statements }
  Params          →  Type id { , Type id } | ε
  Declarations    →  { Declaration }
  Declaration     →  Type  id  ;
  Type            →  int | bool | float
  Statements      →  { Statement }
  Statement       →  ; | Block | Assignment | IfStatement |     
                     WhileStatement |  PrintStmt | ReturnStmt
  ReturnStmt      →  return Expression ;
  Block           →  { Statements }
  Assignment      →  id = Expression ;
  IfStatement     →  if ( Expression ) Statement [ else Statement ]
  WhileStatement  →  while ( Expression ) Statement  
  PrintStmt       →  print(PrintArg { , PrintArg })
  PrintArg        →  Expression | stringlit
  Expression      →  Conjunction { || Conjunction }
  Conjunction     →  Equality { && Equality }
  Equality        →  Relation [ EquOp Relation ]
  Relation        →  Addition [ RelOp Addition ]
  Addition        →  Term { AddOp Term }
  Term            →  Factor { MulOp Factor }
  Factor          →  [ UnaryOp ] Primary
  UnaryOp         →  - | !
  Primary         →  id | intlit | floatlit | ( Expression )
  RelOp           →  < | <= | > | >=   AddOp           →  + | -  MulOp           →  * | / | %  EquOp           →  == | != 
"""


class Parser:
    varDict={}

    def __init__(self, fn: str):

        self.lex = Lexer(fn)
        self.tg = self.lex.token_generator()
        self.currtok = next(self.tg)

    """
        Expr  →  Term { (+ | -) Term }
        Term  → Fact { (* | / | %) Fact }
        Fact  → [ - ] Primary
        Primary  → ID | INTLIT | ( Expr )
        Recursive descent parser. Each non-terminal corresponds 
        to a function.
        -7  -(7 * 5)  -b   unary minus
    """

    # top-level function that will be called
    def program(self) -> Expr:
        """
            Program         →  { FunctionDef }
        """
        funDefs = []
        while self.currtok[0] != "EOF":
            funDefs.append(self.functiondef())
            self.currtok = next(self.tg)
        return Program(funDefs)


    def functiondef(self) -> Expr:
        """
          FunctionDef      Type id ( Params ) { Declarations Statements }
            def __init__(self, t, id:str, params, decls, stmts):
        """

        tmpTpye = self.type()
        self.currtok = next(self.tg)

        tmpID = IDExpr("Identifier")
        self.currtok = next(self.tg)

        if self.currtok[0] == "Lparen":
            self.currtok = next(self.tg)
            params = self.params()  # TODO Keeps changing!
            if self.currtok[0] == "Rparen":
                self.currtok = next(self.tg)

        if self.currtok[0] == "LCbracket":
            self.currtok = next(self.tg)
            decls = self.params()  # TODO Keeps changing!
            self.currtok = next(self.tg)

            stmts = self.statement()
            self.currtok = next(self.tg)

            if self.currtok[0] == "RCbracket":
                self.currtok = next(self.tg)

        left = FunctionDef(tmpTpye, tmpID, params, decls, stmts)

        return left

    def params(self):
        """
        Params          →  Type id { , Type id } | ε
        """
      
        params = []
        if self.currtok[0] != "EOF":
               params.append(" ")
            
        else:
            tmpType = self.type
            self.currtok = next(self.tg)
            params.append(tmpType)
            tmpID = "Identifier"
            
            self.currtok = next(self.tg)
            params.append(tmpID)
            
            while self.currtok[0] == ",":
                tmpType = self.type
                self.currtok = next(self.tg)
                tmpID = "Identifier"
                self.currtok = next(self.tg)
                params.append(tmpType)
                params.append(tmpID)
                self.currtok = next(self.tg)

        return params
    def declarations(self) -> Expr:

        """
               Declarations    →  { Declaration }
        """
        decls = []
        while self.currtok[0] != "EOF":
            decls.append(self.var_declaration())
            self.currtok = next(self.tg)
        return Declarations(decls)

    def var_declaration(self):

        """
               Declaration     →  Type  id  ;
        """
        tmpType = self.type
        self.currtok = next(self.tg)
        if self.currtok[0] == "Identifier":
            tmpID = self.currtok[1]
            if tmpID in self.varDict:
                pass
            else:
                self.varDict[tmpID][0] = tmpType
            self.currtok = next(self.tg)
            if self.currtok[0] == "semicolon":
                return Declaration


    def type(self) -> Expr:
        """
         Type            →  int | bool | float
        """
        if self.currtok[0] == "int":
            tmp = self.currtok
            self.currtok = next(self.tg)
            return IntegerType(tmp[1])
        if self.currtok[0] == "bool":
            tmp = self.currtok
            self.currtok = next(self.tg)
            return BoolType(tmp[1])

        if self.currtok[0] == "float":
            tmp = self.currtok
            self.currtok = next(self.tg)
            return FloatType(tmp[1])

    def statements(self):
        """
        Statements      →  { Statement }
        """
        stmts = []
        while self.currtok[0] != "EOF":
            stmts.append(self.statement())
            self.currtok = next(self.tg)
        return Stmts(stmts)

    def statement(self):

        '''
        Statement       →  ; | Block | Assignment | IfStatement |
                     WhileStatement |  PrintStmt | ReturnStmt
        '''

        if self.currtok[0] == ";":
            self.currtok = next(self.tg)

            # if Block
        if self.currtok[0] == "LCbracket":
            self.currtok = next(self.tg)
            left = self.block()
            return left

            # if Assignment
        if self.currtok[0] == "Identifier":
            left = self.assignment()

            return left
        # IfStatement
        if self.currtok[1] == "if":
            self.currtok = next(self.tg)
            left = self.ifstatement()
            return left

        # WhileStatement
        if self.currtok[1] == "while":
            self.currtok = next(self.tg)
            left = self.whilestatement()
            return left
        # printStatment
        if self.currtok[1] == "print":
            self.currtok = next(self.tg)
            left = self.printStatement()
            return left

        # returnStatment
        if self.currtok[1] == "return":
            self.currtok = next(self.tg)
            left = self.returnStmt()
            return left

    def returnStmt(self):
        """
        ReturnStmt      →  return Expression;
        """
        tree = self.expression()
        return returnStmt(tree)

    def block(self):
        """
        Block           →  { Statements }
        """
        if self.currtok[0] == "LCbracket":
            self.currtok = next(self.tg)
            tree = self.statements()
            if self.currtok[0] == "RCbracket":
                return tree

    def assignment(self) -> Expr:
        """
            Assignment      →  id = Expression;
          """
        key = self.currtok[1]
        self.currtok = next(self.tg)
        if self.currtok[0] == "assignment":
            self.currtok = next(self.tg)
            value = self.expression()
            if key in self.varDict:
                self.varDict[key][1] = value #TODO: type check
            return Assignment(key,value)

    def ifstatement(self):
        """
        IfStatement     →  if ( Expression ) Statement [ else Statement ]
        def __init__(self, cond: Expr, truepart: Stmt, falsepart : Optional[Stmt]):
        pass
        """
        if self.currtok[0] == "Lparen":
            self.currtok = next(self.tg)
            cond = self.expression()  # TODO Keeps changing!

            if self.currtok[0] == "Rparen":
                self.currtok = next(self.tg)
                truePart = self.statement()

            if self.currtok[1] == "else":
                self.currtok = next(self.tg)
                falsePart = self.statement()
                return IfStmt(cond, truePart, falsePart)

            else:
                return IfStmt(cond, truePart,None)

    def whilestatement(self):  # if statment without falsepart
        """
        WhileStatement  →  while ( Expression ) Statement
        """

        if self.currtok[0] == "Lparen":
            self.currtok = next(self.tg)

            cond = self.expression()  # TODO Keeps changing!
            #self.currtok = next(self.tg)

            if self.currtok[0] == "Rparen":
                self.currtok = next(self.tg)
                body = self.statement()
                return WhileStmt(cond,body)

    def printStatement(self):
        """
         PrintStmt       →  print(PrintArg { , PrintArg })
        """
        args = []
        if self.currtok[0] == "Lparen":
            self.currtok = next(self.tg)
            args.append(self.printarg())

            while(self.currtok[0] == "comma"):
                self.currtok = next(self.tg)
                args.append(self.printarg())


            if self.currtok[0] == "Rparen":
                return PrintStmt(args) # TODO have not returned a list of print arguments

    def printarg(self) -> Expr:
        """
          PrintArg        →  Expression | stringlit
        """
        if self.currtok[0] == "Literal String":
            tmp = self.currtok[1]
            self.currtok = next(self.tg)
            return tmp
        else:
            return self.expression()

    def expression(self) -> Expr:
        """
         Expression      →  Conjunction { || Conjunction }
        """

        left = self.conjuntion()


        while self.currtok[0] == "or":
            self.currtok = next(self.tg)
            right = self.conjuntion()
            left = OrExpr(left, right)

        return left

    def conjuntion(self):
        left = self.equality()

        while self.currtok[0] == "and":
            self.currtok = next(self.tg)
            right = self.equality()
            left = AndExpr(left, right)

        return left

    def equality(self) -> Expr:  # a == b      3*z != 99
        # Equality        →  Relation[EquOp Relation]

        left = self.relation()


        if self.currtok[0] in {"equal-equal", "not-equal"}:

            tmp = self.currtok
            self.currtok = next(self.tg)

            right  = self.relation()

            if tmp[0] == "equal-equal":
                left = EqualOp(left, right)
            else:
                left = NOTEqualOp(left, right)
        return left

    def relation(self):  # a < b

        left = self.addition()

        if self.currtok[0] in {"smaller", "smaller-equal", "greater", "greater-equal" }:

            tmp = self.currtok
            self.currtok = next(self.tg)

            right = self.addition()

            if tmp[0] == "smaller":
                left = RelOpLT(left, right)
            elif tmp[0] == "smaller-equal":
                left = RelOpLTE(left, right)
            elif tmp[0] == "greater":
                left = RelOpGT(left, right)

            else:
                left = RelOpGTE(left, right)
        return left

    def addition(self) -> Expr:
        """
        Expr  →  Term { + Term }
        """

        left = self.term()

        while self.currtok[0] in {"plus", "minus"}:
            tmp = self.currtok
            self.currtok = next(self.tg)
            # advance to the next token
            # because we matched a +
            right = self.term()

            if tmp[0] == "plus":
                left = AddExpr(left, right)
            elif tmp[0] == "minus":
                left = minusExpr(left, right)


        return left

    def term(self) -> Expr:
        """
        Term  → Fact { * Fact }
        """
        left = self.fact()

        while self.currtok[0] in {"multiply", "divide"}:
            tmp = self.currtok
            self.currtok = next(self.tg)

            right = self.fact()
            if tmp[0] == "multiply":
                left = MultExpr(left, right)
            else:
                left = DivExpr(left, right)



        return left

    def fact(self) -> Expr:
        """
        Fact  → [ - ] Primary
            e.g., -a  -(b+c)  -6    (b+c) a 6
        """

        # only advance to the next token on a successful match.
        if self.currtok[0] == "minus":
            self.currtok = next(self.tg)
            tree = self.primary()
            return UnaryMinus(tree)

        return self.primary()

    def primary(self) -> Expr:
        """
        Primary  → ID | INTLIT | ( Expr )
        """

        # TODO Add real literals

        # parse an ID
        if self.currtok[0] == "Identifier":  # using ID in expression
            tmp = self.currtok
            # TODO check to make sure ID is declared (in the dictionary)
            self.currtok = next(self.tg)
            return IDExpr(tmp[1])

        # parse an integer literal
        if self.currtok[0] == "Integer":
            tmp = self.currtok
           # self.currtok = next(self.tg)
            return IntLitExpr(tmp[1])

        # parse a parenthesized expression
        if self.currtok[0] == "Lparen":
            self.currtok = next(self.tg)
            tree = self.addition()  # TODO addition -> expression
            if self.currtok[0] == "Rparen":
                self.currtok = next(self.tg)
                return tree
            else:
                # use the line number from your token object
                raise SLUCSyntaxError("ERROR: Missing right paren on line {0}".format(-1))

        # what if we get here we have a problem
        raise SLUCSyntaxError("ERROR: Unexpected token {0} on line {1}".format(self.currtok[1], -1))


# create our own exception by inheriting
# from Python's exception
class SLUCSyntaxError(Exception):
    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


if __name__ == '__main__':
    p = Parser('test.sluc')
    t = p.statements()
    print(t)
