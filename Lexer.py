import sys
from typing import Generator, Tuple
import re

"""
. - the dot character matches any character
#.* - searched for a comment
\s*#.* - comments with whitespace in front including newlines
^ - matches the start of a line
^[ \t]*#.* - look for comments that start a line
^[ \t]*#.*$ - match single line comment
cl.[ds] - match clud and clas
Replace single line comments with a triple quoted string version.
^[ \t]*#(.*)  - single line comment but capture the comment content
                parentheses in a regular expression represent a "capture group"

[_a-zA-Z][_a-zA-Z0-9]*   - match an identifier
\w is shorthand for [_a-zA-Z0-9]
[_a-zA-Z]\w*
What are the rules for an integer constant?
[0-9]+ - integer constant
0[xX][0-9a-fA-F]+   - a hexadecimal constant
"""
#  """\n$1\n""" - replacement text bos where $1 represents the captured value

# sample comment

"""
 sample comment
"""


class Lexer:
    # class variables

    d = {} # empty dictionary

    # Integer:
    d["\d+|\d+[_\d]*\d+"] = "Integer"

    # real number
    d["\d+([_\d]*\d+)?\.?(\d+([_\d]*\d+)?)?e?[\+-]?\d+([_\d]*\d+)?"] = "real number"

    # True/False
    d["True|true|False|false"] = "Keyword"

    # other keyword
    d["print|bool|else|false|if|true|float|int|while|main|char"] = "Keyword"

    # String Literal
    d["^\"\w*\"$"] = "String Literal"

    # operators
    d["\|\|"] = "or"
    d["&&"] = "and"
    d["=="] = "euqal-equal"
    d["!="] = "not-equal"
    d["<"] = "smaller"
    d["<="] = "smaller-equal"
    d[">"] = "greater"
    d[">="] = "greater-equal"
    d['(\+)'] = "plus"
    d['(-)'] = "minus"
    d["\*"] = "multiply"
    d["/"] = "devide"
    d["="] = "assignment"
    d["%"] = "mod"
    d["!"] = "exclamation"
    d[";"] = "semicolon"
    d[","] = "comma"
    d["{"] = "L{"
    d["}"] = "R}"
    d["(\()"] = "Lparen"
    d["(\))"] = "Rparen"
    d["\["] = "L["
    d["\]"] = "R["
    d[">>"] = "shift right"
    d["<<"] = "shift left"
    """
    
    
    
    
    
"""
    # Identifier
    d["^[a-zA-Z_]\w*"] = "Identifier"





    '''
    INTLIT = 0  # codes for the "kind" of value
    PLUS = 1
    ID = 2
    LPAREN = 3
    RPAREN = 4
    INTEGER = 5
'''
    # fn - file name we are lexing
    def __init__(self, fn: str):

        try:
            self.f = open(fn)
        except IOError:
            print("File {} not found".format(fn))
            print("Exiting")
            sys.exit(1)  # can't go on

    def token_generator(self) -> Generator[Tuple[int, str, int], None, None]:
        """
        Returns the tokens of the language
        """

        # backslash plague - eliminated because of python raw strings
        split_patt = re.compile(r"(\+)|\s|(\()|(\))")  # parentheses around a pattern
        # captures the value

        # a more readable way to write the split
        # pattern above using the VERBOSE option
        split_patt = re.compile(
            r"""             # Split on 
               ((?<!e)\+) |        #  plus and capture
               ((?<!e)-) |         #  minus and capture, minus not special unless in []
               ([=><!]=|=)  |   # ==, >=, <=, != and capture
              #(".+~\"$) |    # Literal String
               \s   |        #  whitespace
               (\() |        #  left paren and capture
               (\))  |       #  right paren and capture
               ({)   |      # right { and capture
               (})   |      # left } and capture
               (\[)   |      # right [ and capture
               (\])   |     # left ] and capture
               (,)    |     # comma and capture
               (;)    |     #semicolon and capture
               (!)    |     #exclamation and capture
               (%)  |
               (\*) |
               (/)  |
               (>>)  |
               (<<) 
              
            """,
            re.VERBOSE
        )


        for i, line in enumerate(self.f, start=1):
            # skip over comment
            new_line = re.sub("//.*"," ", line)
            String_pattern = re.compile("\"(.*?)\"")
            literal_string = String_pattern.finditer(new_line)
            if (literal_string != None):
                for c in literal_string:
                    #print(new_line[c.start():c.end()])
                    #　it will generate extra \ if the string ends with \
                    yield  "Literal String" , new_line[c.start():c.end()], i
            else:
                print("None")


          #  yield
            new_line = re.sub("\".*?\"", " ", new_line)
            tokens = (t for t in split_patt.split(new_line) if t)
            for t in tokens:
              #  try:
                for k,v in Lexer.d.items():
                    if (re.fullmatch(k,t)!= None):
                        yield v, t, i
                        break

                #except:
                   # print("I can't find this")




if __name__ == "__main__":

    print(re.match("(^e)","a"))
    s = "He said \"go\""
    print(s)
    print(re.search("\"(.+?)\"", s))
    print(re.sub("//.*"," ","comment// This is comment"))
    String_patter = re.compile(r"(~\\)\".*?(~\\)\"")
    literal_strin = String_patter.search(s)
    print(literal_strin)

   # lex = Lexer(sys.argv)
    lex = Lexer("test2.sluc")

    g = lex.token_generator()

    print("%-35s %-30s %s" % ("Token", "Name", "Line Number"))
    print("--------------------------------------------------------------------------------------")


    while True:



        try:
            for i in next(g):
               print("%-25s"%(i), "\t\t\t",end="")
            print("")
        except StopIteration:
            print("Done")
            break
