import sys
from typing import Generator, Tuple
import re


class Lexer:
    # class variables
    # create a dictionary to present tokens
    d = {} # empty dictionary

    # literal string
    d["Literal String"] =r"(\"(?:[^\\\"]|\\.)*\")"

    # Integer:
    d["Integer"] = "\d+|\d+[_\d]*\d+"

    # real number
    d["real number"] = "\d+([_\d]*\d+)?\.?(\d+([_\d]*\d+)?)?e?[\+-]?\d+([_\d]*\d+)?"

    # Keyword
    d["Keyword"] = "True|true|False|false|print|bool|else|false|if|true|float|int|while|main|char"

    # operators
    d["or"] = "\|\|"
    d["and"] = "&&"
    d["equal-equal"] = "=="
    d["not-equal"] = "!="
    d["smaller"] = "<"
    d["smaller-equal"] = "<="
    d["greater"] = ">"
    d["greater-equal"] = ">="
    d["plus"] = "(\+)"
    d["minus"] = '(-)'
    d["multiply"] = "\*"
    d["devide"] = "/"
    d["assignment"] = "="
    d["mod"] = "%"
    d["exclamation"] = "!"

    #punctuation
    d["semicolon"] = ";"
    d["comma"] = ","
    d["LCbracket"] = "{"
    d["RCbracket}"] = "}"
    d["Lparen"] = "(\()"
    d["Rparen"] = "(\))"
    d["LSbracket"] = "\["
    d["RSbracket["] = "\]"
    d["shift right"] = ">>"
    d["shift left"] = "<<"

    # Identifier
    d["Identifier"] = "^[a-zA-Z_]\w*"



    def __init__(self, fn: str):
        try:
            self.f = open(fn)
        except IOError:
            print("File {} not found".format(fn))
            print("Exiting")
            sys.exit(1)  # can't go on

        """
        # if there are 2 system argument(one of them is Lexer.py), run the program
        if len(arg) >= 2:
            try:
                self.f = open(arg[1])
            # throw IOError if file name is wrong/ file does not exist
            except IOError:
                print("File {} not found".format(arg[1]))
                print("Exiting")
                sys.exit(1)  # can't go on
        # exit with error message if there are more than one input files
       # elif len(arg) > 2:
           # print("Expect 1 argument, given ", len(arg)-1)
           # print("Exiting")
           # sys.exit(1)
        # exit with error message if there is not input file
        else:
            print("there is not input file")
            print("Exiting")
            sys.exit(1)
        """

    def token_generator(self) -> Generator[Tuple[int, str, int], None, None]:
        """
        Returns the tokens of the language
        """

        # a more readable way to write the split
        # pattern above using the VERBOSE option
        split_patt = re.compile(
            r"""             # Split on 
               (\"(?:[^\\\"]|\\.)*\")|   # Literal String   
               [ \t]*//.*|               # comment
               ((?<!e)\+) |              #  plus and capture
               ((?<!e)-) |               #  minus and capture, minus not special unless in []
               ([=><!]=|=)  |   # ==, >=, <=, != and capture
               \s   |        #  whitespace
               (\() |        #  left paren and capture
               (\))  |       #  right paren and capture
               ({)   |      # right curly brackets and capture
               (})   |      # left curly brackets and capture
               (\[)   |      # right square brackets and capture
               (\])   |     # left square brackets and capture
               (,)    |     # comma and capture
               (;)    |     # semicolon and capture
               (!)    |     # exclamation and capture
               (%)  |       # mod and capture
               (\*) |       # star and capture
               (/)  |       # slash and capture
               (>>)  |      # shift right and capture
               (<<)         #shift left and capture
            """,
            re.VERBOSE
        )
        # go through every line in the input file
        for i, line in enumerate(self.f, start=1):
            #  go through every token in line
            tokens = (t for t in split_patt.split(line) if t)
            for t in tokens:
                # search for match-pattern in the dictionary
                for k, v in Lexer.d.items():
                    # if it match, yield token,name and line #
                    if re.fullmatch(v, t) != None:
                        yield k, t, i
                        break
                # if it can not match any pattern in the dictionary, yield error message and line #
                else:
                    yield "Error: illegal token", t, i
        yield "EOF","",""


if __name__ == "__main__":

    lex = Lexer("test.sluc")

    g = lex.token_generator()

    # print the header for the output table
    print("%-35s %-85s %s" % ("Token", "Name", "Line Number"))
    print(
        "--------------------------------------------------------------------------------------------------------------------------------------")
    # setup a list for the interval between column
    format_lst = ["%-35s", "%-80s", "%s"]

    while True:
        try:
            # print output table
            for j, i in enumerate(next(g), start=0):
                print(format_lst[j] % (i), "\t", end="")
            print("")
        except StopIteration:
            print("Done")
            break