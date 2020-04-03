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
    # check whether we can combine them later
    d["\d+"] = "Integer"  # without underscore
    d["\d+(_)*\d*[(_)]\d+"]="Integer"  # with underscore

    # Real Number
    # check whether we can combine them later
    d["\d+[.(e.)][\+\-]?\d+"] = "Real Number" # without underscore, without +/-
    d["\d+(_)*\d*[(_)]\d+[.(e.)][\+\-]?\d+(_)*\d*[(_)]\d+"] = "Real Number" # with underscore


    # True/False
    d["True|true|False|false"] = "Keyword"



    # String Literal


    #d["\w"] = "String Literal"
   # d[] = "Comment"
    d["^(//).*"] = "Comment"
    #d[] = "Identifier"

    d['(\+)'] = "Plus"
    d['(-)'] = "Minus"
    d["(\()"] = "Lparen"
    d["(\))"] = "Rparen"

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

    def token_generator(self) -> Generator[Tuple[int, str], None, None]:
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
               (~e\+) |        #  plus and capture
               (~e-) |         #  minus and capture, minus not special unless in []
               (=)  |
               (\\\w+\n) |
               \s   |        #  whitespace
               (\() |        #  left paren and capture
               (\))          #  right paren and capture
              
            """,
            re.VERBOSE
        )


        for i, line in enumerate(self.f, start=1):
            tokens = (t for t in split_patt.split(line) if t)
            for t in tokens:
              #  try:
                for k,v in Lexer.d.items():
                    if (re.fullmatch(k,t)!= None):
                        yield t, v, i
                        break

                #except:
                   # print("I can't find this")




if __name__ == "__main__":
    print(re.fullmatch("^(//).*","//hello world"))
    print(re.fullmatch("[0-9a-zA-Z_]*",".4"))
    lex = Lexer("test.sluc")

    g = lex.token_generator()


    while True:
        try:
            print(next(g))
        except StopIteration:
            print("Done")
            break
