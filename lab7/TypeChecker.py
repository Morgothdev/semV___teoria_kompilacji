# -*- coding: utf-8 -*-

from AST import *
from SymbolTable import *
from OperationsTable import OperationsTable as OT
from DEBUG import *

class TypeChecker:

    def __init__(self):
        self.symbolTable = None
        self.operationsTable = OT()
        self.errors = 0

    def raiseError(self, body):
        self.errors += 1
        print body

    @staticmethod
    def typesAreCoherent(should, beType):
        if DEBUG.debug: print "should",should,"|","beType", beType
        return beType == should or (beType == 'float' and should=='int')

    def acceptOrVar(self, node):
        if node.__class__.__name__ == 'str':
            variable = self.symbolTable.get(node)
            return None if variable is None else variable.type
        else:
            return node.accept(self)

    def analyzeDeclarations(self, declarationsList):
        for varList in declarationsList:
            if varList.accept(self):
                Type = varList.typ
                for var in varList.variables:
                    try:
                        self.symbolTable.put(var.left, VariableSymbol(var.left, Type, var))
                    except Exception:
                        self.raiseError("(linia "+str(var.lineno)+"): Podwójna deklaracja \""+var.left+"\", poprzednia deklaracja w linii"+str(self.symbolTable.get(var.left).lineno())+".")

    def analyzeFunctionDeclarations(self, declarationsList):
        for funDef in declarationsList:
            self.symbolTable.put(funDef.ident, FunctionSymbol(funDef.ident, funDef.typ, funDef.args, funDef))
            if funDef.accept(self) is None:
                self.raiseError("(linia "+str(var.lineno)+"): Błędy w definicji funkcji "+funDef.ident+".")

    def analyzeInstructionBlock(self, block):

        if block.__class__.__name__ == 'CompoundInstruction':
            return self.visit_CompoundInstruction(block)
        elif block.__class__.__name__ == 'list':
            return self.analyzeInstructions(block)
        elif isinstance(block,Node):
            return block.accept(self)
        else:
            raise Exception("jakie jeszcze bloki instrukcji tu wejdą?")

    def analyzeInstructions(self, instructionsList):
        for instr in instructionsList:
            instr.accept(self)

    def analyzeCondExpr(self, expr):
        condType = expr.accept(self)
        if condType != 'int':
            self.raiseError("(linia "+str(expr.lineno)+"): Nieprawidłowy typ wyrażenia warunkowego.")
    
    def visit_BinExpr(self, node):
        if DEBUG.debug: print "visiting BinExpr in line",node.lineno
        leftType = self.acceptOrVar(node.left)
        rightType = self.acceptOrVar(node.right)
        op = node.op;
        if leftType is None:
            self.raiseError("(linia "+str(node.lineno)+"): Nie rozpoznano typu lewej strony.")
        if rightType is None:
            self.raiseError("(linia "+str(node.lineno)+"): Nie rozpoznano typu prawej strony.")
        if rightType is not None and leftType is not None:
            Type = self.operationsTable.getOperationType(op,leftType,rightType)
            if Type is None:
                self.raiseError("(linia "+str(node.lineno)+"): Nieobsługiwana operacja " +leftType+" "+op+" "+rightType+".")
            return Type

    def visit_Assignment(self, assInstr):
        if DEBUG.debug: print "visit_Assignment in line",assInstr.lineno
        if assInstr.left.__class__.__name__ != 'str':
            self.raiseError("(linia "+str(assInstr.lineno)+"): Lewa strona przypisania musi być identyfikatorem.")
        leftType = self.symbolTable.get(assInstr.left).type
        rightType = self.acceptOrVar(assInstr.right)
        if leftType is None:
            self.raiseError("(linia "+str(assInstr.lineno)+"): Użyto niezadeklarowanej nazwy "+assInstr.left+".")
        if rightType is None:
            self.raiseError("(linia "+str(assInstr.lineno)+"): Nie rozpoznano typu wartości przypisywanej.")
        if rightType is not None and leftType is not None:
            if not TypeChecker.typesAreCoherent(should=rightType,beType=leftType):
                self.raiseError("(linia "+str(assInstr.lineno)+"): Nieprawidłowy typ wartości przypisywanej, wymagany "+leftType+", znaleziony "+rightType+".")

    def visit_CompoundInstruction(self, compInstr):
        if DEBUG.debug: print "visit_CompoundInstruction in line",compInstr.lineno
        prevTable = self.symbolTable
        self.symbolTable = SymbolTable(prevTable,"compInstr("+str(compInstr.lineno)+") scope")
        self.analyzeDeclarations(compInstr.decl)
        self.analyzeInstructionBlock(compInstr.instr)
        symbolTable = self.symbolTable
        self.symbolTable = prevTable
        return symbolTable

    def visit_WhileLoop(self, whLoop):
        if DEBUG.debug: print "visit_WhileLoop in line",whLoop.lineno
        self.analyzeCondExpr(whLoop.cond)
        whLoop.instr.accept(self)

    def visit_RepeatUntilLoop(self, repeatLoop):
        if DEBUG.debug: print "visit_RepeatUntilLoop in line",repeatLoop.lineno
        self.analyzeInstructionBlock(repeatLoop.instr)
        self.analyzeCondExpr(repeatLoop.cond)

    def visit_RelExpr(self, node):
        if DEBUG.debug: print "visit_RelExpr in line",node.lineno
        type1 = self.acceptOrVar(node.left)
        type2 = self.acceptOrVar(node.right)
        op = node.op 
        if type1 is None:
            self.raiseError("(linia "+str(node.lineno)+"): Typ wyrażenia po lewej nie rozpoznawalny.")
        if type2 is None:
            self.raiseError("(linia "+str(node.lineno)+"): Typ wyrażenia po prawej nie rozpoznawalny.")
        return self.operationsTable.getOperationType(op,type1,type2)

    def visit_Program(self, program):
        if DEBUG.debug: print "visit_Program in line",program.lineno
        self.symbolTable = SymbolTable(None,"program scope")
        
        self.analyzeDeclarations(program.decl)
        self.analyzeFunctionDeclarations(program.fundef)
        self.analyzeInstructionBlock(program.instr)

        if DEBUG.debug: print "symbolTable: ", self.symbolTable.currentScope
        return self.errors is 0

    #zbadanie poprawności listy zmiennych
    def visit_Variable(self, variable):
        if DEBUG.debug: print "visit_Variable in line",variable.lineno
        Type = variable.typ
        result = True
        for var in variable.variables:
            valueType = var.right.accept(self)
            if not TypeChecker.typesAreCoherent(should=valueType,beType=Type):
                self.raiseError("(linia "+str(var.lineno)+"): Niekompatybilna inicjacja zmiennej "+var.left+", wymagany "+Type+", znaleziony "+valueType)
                result = False
        return result

    def visit_Float(self, var):
        if DEBUG.debug: print "visit_Float in line",var.lineno
        return 'float'

    def visit_Integer(self, var):
        if DEBUG.debug: print "visit_Integer in line",var.lineno
        return 'int'

    def visit_String(self, var):
        if DEBUG.debug: print "visit_String in line",var.lineno
        return 'string'


    def visit_Print(self, instr):
        if DEBUG.debug: print "visit_Print in line",instr.lineno
        Type = self.acceptOrVar(instr.expr)
        if Type is None:
            self.raiseError("(linia "+str(instr.lineno)+"): Typ argumentu nie rozpoznawalny.")

    def visit_Argument(self, arg):
        if DEBUG.debug: print "visit_Argument in line",arg.lineno
        return arg.typ

    def visit_FunctionCall(self, funCall):
        if DEBUG.debug: print "visit_FunctionCall in line",funCall.lineno
        funDef = self.symbolTable.get(funCall.ident)
        if funDef is None:
            self.raiseError("(linia "+str(funCall.lineno)+"): Funkcja "+funCall.ident+" nie istnieje.")
            return None

        # if len(funDef.args) != funCall.args:
        #     self.raiseError("(linia "+str(funCall.lineno)+"): Nieprawidłowa ilość arguentów podanych do wywołania funkcji "+funCall.ident)
        #     return None

        for left, right in zip(funDef.args,funCall.args):
            defType = left.accept(self)
            callType = self.acceptOrVar(right)
            #print left,right,defType, callType
            if not TypeChecker.typesAreCoherent(should=callType, beType=defType):
                self.raiseError("(linia "+str(funCall.lineno)+"): Niewłaściwy typ parametru, wymagany "+defType+", znaleziony "+callType+".")
        return funDef.type
            

    def visit_ChoiceInstruction(self, instr):
        if DEBUG.debug: print "visit_ChoiceInstruction in line",instr.lineno
        self.analyzeCondExpr(instr.cond)
        self.analyzeInstructionBlock(instr.instr)
        
    def visit_ChoiceInstructionWithElse(self, instr):
        if DEBUG.debug: print "visit_ChoiceInstructionWithElse in line",instr.lineno
        self.visit_ChoiceInstruction(instr)
        self.analyzeInstructionBlock(instr.elinstr)

    def visit_FunctionDefinition(self, funDef):
        if DEBUG.debug: print "visit_FunctionDefinition in line",funDef.lineno
        prevTable = self.symbolTable
        self.symbolTable = SymbolTable(prevTable, "fundef("+funDef.ident+") scope")
        
        for arg in funDef.args:
            self.symbolTable.put(arg.ident, VariableSymbol(arg.ident, arg.typ, arg))
    
        functionsBodySymbolTable = self.analyzeInstructionBlock(funDef.instr)

        self.symbolTable = functionsBodySymbolTable

        instrs = filter(lambda x: x.__class__.__name__ =='Return', funDef.instr.instr)
        for retInstr in instrs:
            valueType = retInstr.accept(self)
            if valueType is None:
                print "(linia "+str(retInstr.lineno)+"): Niekompatybilny zwracany typ z intrukcji return, użyto niezadeklarowanej zmiennej",retInstr.value
            elif valueType != funDef.typ:
                print "(linia "+str(retInstr.lineno)+"): Niekompatybilny zwracany typ z intrukcji return, wymagany",funDef.typ+", znaleziony",valueType
        
        self.symbolTable = prevTable

        return funDef.typ

    def visit_Return(self, ret):
        if DEBUG.debug: print "visit_Return in line",ret.lineno
        return self.acceptOrVar(ret.value)