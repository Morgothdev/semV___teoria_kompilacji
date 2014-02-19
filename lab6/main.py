# -*- coding: utf-8 -*-

import sys
import ply.yacc as yacc
from Cparser import Cparser
from TypeChecker import TypeChecker

if __name__ == '__main__':

     try:
          filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
          file = open(filename, "r")
     except IOError:
          print("Cannot open {0} file".format(filename))
          sys.exit(0)

     
     Cparser = Cparser()
     checker = TypeChecker()
     parser = yacc.yacc(module=Cparser)
     text = file.read()
     ast = parser.parse(text,lexer=Cparser.scanner)
     
     if not Cparser.error:
          if ast.accept(checker):
               print "Wszystko jest ok."
          else:
               print "Znaleziono błędy."
     else:
          print "Wystapily bledy podczas parsingu"
