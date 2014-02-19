# -*- coding: utf-8 -*-

import sys
import ply.yacc as yacc
from Cparser import Cparser
from TypeChecker import TypeChecker
from Interpreter import Interpreter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()

    ast = parser.parse(text, lexer=Cparser.scanner)
 
    # jesli wizytor TypeChecker z implementacji w poprzednim lab korzystal z funkcji accept
    # to nazwa tej ostatniej dla Interpretera powinna zostac zmieniona, np. na accept2 ( ast.accept2(Interpreter()) )
    # tak aby rozne funkcje accept z roznych implementacji wizytorow nie kolidowaly ze soba
    
    checker = TypeChecker()
    ast.accept(checker)
    if checker.errors == 0:
        ast.acceptInterpreter(Interpreter())
    else:
        print "TypeChecker znalazł błędy."

    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())
   
