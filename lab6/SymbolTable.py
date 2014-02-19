 # -*- coding: utf-8 -*-

from DEBUG import *

class Symbol:
    def __init__(self, Type, Node):
        self.type = Type
        self.node = Node

    def lineno(self):
        return self.node.lineno

    def __repr__(self):
        return self.__class__.__name__ + ", type "+str(self.type)

class ConstSymbol(Symbol):
    def __init__(self, Type, Node):
        Symbol.__init__(Type, Node)

    def __repr__(self):
        return Symbol.__repr__(self)


class VariableSymbol(Symbol):
    def __init__(self, Name, Type, Node):
        Symbol.__init__(self,Type, Node)
        self.name = Name

    def __repr__(self):
        return Symbol.__repr__(self) + ", name "+str(self.name)

class FunctionSymbol(VariableSymbol):
    def __init__(self, Name, Type, Args, Node):
        VariableSymbol.__init__(self, Name, Type, Node)
        self.args = Args
    
    def __repr__(self):
        return Symbol.__repr__(self)


"""
czyli to ma być tablica, w której będę sobie przechowywał aktualny zbiór zmiennych
cos więcej?
"""
class SymbolTable(object):

    def __init__(self, Parent, name="nie wiem"):
        self.currentScope = {}
        self.parent = Parent
        self.name = name


    def put(self, name, symbol):
        if DEBUG.debug: print "added name",name,"with symbol",symbol,"in scope",self.name
        if name in self.currentScope: raise Exception("podwójna deklaracja")
        else: self.currentScope[name] = symbol

    def get(self, name):
        if name not in self.currentScope: return ((self.parent.get(name) if self.parent is not None else None))
        else: return self.currentScope[name]

    def getParentScope(self):
        return self.parent

    def printSelf(self):
        if self.parent is not None:
            self.parent.printSelf()
        print self.name,self.currentScope