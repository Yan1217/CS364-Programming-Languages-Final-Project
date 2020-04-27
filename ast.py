"""
SLU-C Abstract Syntax Trees
An abstract syntax tree (AST) is a data structure that represents
the concrete (text) syntax of a program
"""
from typing import Sequence, Union, Optional

# Use a class hierarchy to represent types.





class Expr:
    """
    Base class for expressions
    """

    pass

class Type:
    pass

class IntegerType(Type):
    def __init__(self, type: int):
        self.type = type
    def __str__(self):
        return str(self.type)

class FloatType(Type):
    def __init__(self, type: float):
        self.type = type
    def __str__(self):
        return str(self.type)
class BoolType(Type):
    def __init__(self, type: bool):
        self.type = type
    def __str__(self):
        return str(self.type)

class Program:
    def __init__(self,funDefs:[]):
        self.funDefs = funDefs

    def __str__(self):
        return "".join("{}".format(x) for x in self.funDefs)


class FunctionDef:
    def __init__(self, t, id:str, params, decls, stmts):
        # provide type hints for all of the parameters
        # Decls should be a dictionary
        # Key: id
        # Value: Type
        pass

    def __str__(self):
        pass

    def eval(self) -> Union[int, float, bool]:
        # an environment maps identifiers to values
        # parameters or local variables
        # to evaluate a function you evaluate all of the statements
        # within the environment
        env = {}   # TODO Fix this
        for s in self.stmts:
            s.eval(env)  # TODO define environment



class Stmt:
    pass
class Stmts(Stmt):
    def __init__(self, statements: []):
        self.stmts = statements

    def __str__(self):
        return "\n".join("{}".format(x) for x in self.stmts)

class returnStmt(Expr):
    def __init__(self, stmt: Expr):
        self.stmt = stmt

    def __str__(self):
        return "return {0}".format(str(self.stmt))

class Assignment(Expr):
    def __init__(self, id:str, assign: Expr):
        self.id = id
        self.assign = assign

    def __str__(self):
        return "{0} = {1}".format(str(self.id),str(self.assign))

class IfStmt(Stmt):
    def __init__(self, cond: Expr, truePart: Stmt, falsePart : Optional[Stmt]):
        self.cond = cond
        self.truePart = truePart
        self.falsePart = falsePart

    def __str__(self):
        if self.falsePart==None:
            return "if {0}   {1}".format(str(self.cond),str(self.truePart))
        else:
            return "if {0}   {1} else  {2}".format(str(self.cond),str(self.truePart),str(self.falsePart))

class WhileStmt:
    def __init__(self,cond:Expr, body:Stmt):
        self.cond = cond
        self.body = body

    def __str__(self):
        return "while {0}:\n \t{1}".format(str(self.cond),str(self.body))

class PrintStmt:
    def __init__(self, printitem:[] ):
        self.printitem = printitem

    def __str__(self):
        return "print("+"".join('{:3s}, '.format(x) for x in self.printitem)+")"

class Declaration:
    def __init__(self, type:str, id:str):
        self.type = type
        self.id = id

    def __str__(self):
        return "{0} {1};".format(str(self.type),str(self.id))


class Declarations(Declaration):
    def __init__(self, declarations: []):
        self.declarations = declarations

    def __str__(self):
        return "\n".join("{}".format(x) for x in self.declarations)


# TODO Don't just cut-and-paste new operations, abstract!

class BinOpP(Expr): # Binary Operation super class

    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right
        self.op = ""

    def __str__(self):
        return "({0} {1} {2})".format(str(self.left), self.op, str(self.right))


class OrExpr(BinOpP):
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.op = "||"

class AndExpr(BinOpP):
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.op = "&&"


    # def typeof(self) -> str: # where string is 'int' or 'float' or 'bool' or 'error'
    # strings are not abstract "INT" "int" "fred"
    # Expressions have types
    #def typeof(self) -> Type:
    def typeof(self) -> Union[int, bool, float]:   #
        """
        Return the type of the expression.
        1) 4 + 4 is an int
        2) 2 * 3.14 is a float
        3) True && False is a bool
        4) True && 3.14 type error
        Static type checking: type check the program *before* we evaluate it.
        Scheme is dynamically type checked. Type errors checked at run time.
        Java - statically type checked.
        C - static
        Python - dynamic, checked at run time
                 mypy - static type checker for Python
        """
        if self.left.typeof() == BoolType and self.right.typeof() == BoolType:
            return BoolType
        else:
            # type error
            raise SLUCTypeError(
                "type error on line {0}, expected two booleans got a {1} and a {2}".format(0))

class SLUCTypeError(Exception):
    def __init__(self, message: str):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


class EqualOp(BinOpP):
    def __init__(self,left:Expr, right:Expr):
        super().__init__(left, right)
        self.op = "=="

    def scheme(self) -> str:
        return "(== {0} {1})".format(self.left.scheme(), self.right.scheme())

    def eval(self) -> Union[int,float]:
        # TODO environment
        return self.left.eval() +  self.right.eval()


class NOTEqualOp(BinOpP):
    def __init__(self,left:Expr, right:Expr):
        super().__init__(left, right)
        self.op = "!="

class AddExpr(BinOpP):
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.op = "+"
class minusExpr(BinOpP):
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.op = "-"


class RelOpLT(BinOpP):
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.op = "<"

class RelOpGT(BinOpP):
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.op = ">"

class RelOpGTE(BinOpP):
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.op = ">="
class RelOpLTE(BinOpP):
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.op = "<="

class MultExpr(BinOpP):
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.op = "*"

    def scheme(self):
        """
        Return a string that represents the expression in Scheme syntax.
        e.g.,  (a * b)   -> (* a b)
        """
        return "(* {0} {1})".format(self.left.scheme(), self.right.scheme())

    def eval(self) -> Union[int,float]:
        # TODO environment
        # Implementing SLU-C multiplication using Python's multiplication
        # implmented * using mul instruction

        # If we checked type when running eval we have a "dynamically typed"
        # language

        return self.left.eval() *  self.right.eval()

class DivExpr(BinOpP):
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right)
        self.op = "/"

class UnaryMinus(Expr):
    def __init__(self, tree: Expr):
        self.tree = tree

    def __str__(self):
        return "-({0})".format(str(self.tree))

    def scheme(self):
        return "(- {0})".format(self.tree.scheme())

    def eval(self):
        return -self.tree.eval()

class IDExpr(Expr):

    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id

    def scheme(self):
        return self.id

    def eval(self, env):  # a + 7
        # lookup the value of self.id. Look up where?
        # env is a dictionary
        pass

    def typeof(self, decls) -> Type:
        # TODO type decls appropriately as a dictionary type
        # look up the variable type in the declaration dictoinary
        # from the function definition (FunctionDef)
        pass


class StrlitExpr(Expr):
    def __init__(self, strlit: str):
        self.strlit = strlit

    def __str__(self):
        return str(self.strlit)

class IntLitExpr(Expr):

    def __init__(self, intlit: str):
        self.intlit = int(intlit)

    def __str__(self):
        return str(self.intlit)

    def scheme(self):
        return str(self.intlit)

    def eval(self):
        return self.intlit   # base case

    #def typeof(self) -> Type:
    # representing SLU-C types using Python types
    def typeof(self) -> type:

        #return IntegerType
        return int

if __name__ == '__main__':
    """
    Represent a + b + c * d
    ((a + b) + (c * d))
    """
    expr = EqualOp(AddExpr(IDExpr('a'), IDExpr('b')),
                   MultExpr(IDExpr('c'), IDExpr('d')))
    print(expr)