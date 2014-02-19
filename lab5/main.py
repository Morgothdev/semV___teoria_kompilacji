import sys
import ply.yacc as yacc
from TreePrinter import *
from Cparser import Cparser

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc( module=Cparser )
    text = file.read()
    parser.parse(text, lexer=Cparser.scanner)


    if(Cparser.errors>0):
        print "Parser collects {0} error{1}. Input is not valid!".format(Cparser.errors, "" if Cparser.errors==1 else "s")
    else:
        print Cparser.tree