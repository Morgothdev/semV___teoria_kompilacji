# -*- coding: utf-8 -*-

from AST import *
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
from DEBUG import DEBUG

operators = {
'+': lambda x,y : x+y, '-': lambda x,y : x-y,'*': lambda x,y: x*y, 
'/': lambda x,y : x/y, '%': lambda x,y : x%y, 

'^': lambda x,y : x^y, '|': lambda x,y : x|y, '&': lambda x,y : x&y,
'SHL': lambda x,y: x<<y, 'SHR': lambda x,y: x>>y,

'OR': lambda x,y : x or y, 'AND': lambda x,y : x and y, 
'<=': lambda x,y: not (x>y), '>=': lambda x,y: x>=y, 
'<': lambda x,y : x<y, '>': lambda x,y : x>y, 
'==': lambda x,y: x==y, '!=': lambda x,y: not x==y}

class Interpreter(object):

    def __init__(self):
        self.memoryStack = MemoryStack()
        self.functions = FunctionMemory()

    @on('node')
    def visit(self, node):
        print "visit",node

    def acceptOrVar(self, node):
        if node.__class__.__name__ == 'str':
            variable = self.memoryStack.get(node)
            return variable
        else:
            returnFromAccepted = node.acceptInterpreter(self)
            return returnFromAccepted

    def makeMemoryFromDeclarations(self, name, declarations):
        memory = Memory(name)
        for declaration in declarations:
            for var in declaration.variables:
                initValue = self.acceptOrVar(var.right)
                memory.put(var.left, initValue)
        return memory

    def interpretInstructionBlock(self, block):
        if block.__class__.__name__ == 'list':
            self.interpretInstructions(block)
        elif isinstance(block,Node):
            block.acceptInterpreter(self)
        else:
            raise Exception("jakie jeszcze bloki instrukcji tu wejdą?")

    def interpretInstructions(self, instructionsList):
        for instr in instructionsList:
            instr.acceptInterpreter(self)

    @when(Program)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit Program", node, "in line",node.lineno
        globalMemory = self.makeMemoryFromDeclarations("programStack",node.decl)
        self.memoryStack.push(globalMemory)
        self.functions.pushGlobalMemory(globalMemory)
        for funDef in node.fundef: funDef.acceptInterpreter(self)
        self.interpretInstructionBlock(node.instr)

    @when(FunctionDefinition)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit FunctionDefinition", node, "in line",node.lineno
        memory = Memory("arguments of "+node.ident)
        for arg in node.args:
            memory.put(arg.ident,None)
        self.functions.putFunction(node.ident, memory, node)

    @when(FunctionCall)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit FunctionCall", node, "in line",node.lineno
        funDef = self.functions.getFunction(node.ident)
        
        argumentsList = node.args
        callMemory = Memory("call gcd")
        for defArg, passedArg in zip(funDef.args,argumentsList):
            callMemory.put(defArg.ident, self.acceptOrVar(passedArg))
        
        prevStack = self.memoryStack
        self.memoryStack = self.functions.getStack(node.ident, callMemory)
        try:
            funDef.instr.acceptInterpreter(self)
        except ReturnException as ret:
            self.memoryStack = prevStack
            return ret.value

        self.memoryStack = prevStack
        raise Exception("No return statement in function "+node.ident)

    # Nie wiem dlaczego tutaj był return, zdaje się, żę ten język nie jest wyrażeniowy
    # więc blok instrukcji nie zwraca wartości.... Wywalam.
    @when(WhileLoop)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit WhileLoop", node, "in line",node.lineno
        try:
            while True:
                breakIf = node.cond.acceptInterpreter(self)
                if not breakIf: break
                try:
                    node.instr.acceptInterpreter(self)
                except ContinueException:
                    if DEBUG.debugInterpreter: print "continue"
        except BreakException:
            if DEBUG.debugInterpreter: print "break"

    @when(RepeatUntilLoop)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit RepeatUntilLoop", node, "in line",node.lineno
        try:
            while True:
                try:
                    r = node.instr.acceptInterpreter(self)
                except ContinueException:
                    if DEBUG.debugInterpreter: print "continue"
                if node.cond.acceptInterpreter(self): break
        except BreakException:
            if DEBUG.debugInterpreter: print "break"

    @when(CompoundInstruction)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit CompoundInstruction", node, "in line",node.lineno
        self.memoryStack.push(self.makeMemoryFromDeclarations("compInstr("+str(node.lineno)+") scope",node.decl))
        self.interpretInstructionBlock(node.instr)
        return self.memoryStack.pop()     

    @when(Break)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit Break", node, "in line", node.lineno
        raise BreakException()

    @when(Continue)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit Continue", node, "in line", node.lineno
        raise ContinueException()

    @when(Print)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit Print", node, "in line", node.lineno
        print self.acceptOrVar(node.expr)

    @when(Return)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit Return", node, "in line", node.lineno
        value = self.acceptOrVar(node.value)
        raise ReturnException(value)

    @when(RelExpr)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit RelExpr", node, "in line", node.lineno
        r1 = self.acceptOrVar(node.left)
        r2 = self.acceptOrVar(node.right)
        result = operators[node.op](r1,r2)
        if not isinstance(result, bool):
            raise Exception("not bool operator: "+node.op+" in line "+node.lineno)
        return result
    
    @when(BinExpr)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit BinExpr", node, "in line",node.lineno
        r1 = self.acceptOrVar(node.left)
        r2 = self.acceptOrVar(node.right)
        result = operators[node.op](r1,r2)
        if not isinstance(result, (int, long, float)):
            raise Exception("not numeric operator: " + node.op + " in line " + node.lineno)
        return result

    @when(Assignment)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit Assignment", node, "in line", node.lineno
        varName = node.left
        value = self.acceptOrVar(node.right)
        self.memoryStack.put(varName, value)

    @when(Const)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit Const", node, "in line", node.lineno
        return node.value

    @when(ChoiceInstruction)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit ChoiceInstruction", node, "in line", node.lineno
        if node.cond.acceptInterpreter(self):
            node.instr.acceptInterpreter(self)

    @when(ChoiceInstructionWithElse)
    def visit(self, node):
        if DEBUG.debugInterpreter: print "Interpreter visit ChoiceInstructionWithElse", node, "in line", node.lineno
        if node.cond.acceptInterpreter(self):
            node.instr.acceptInterpreter(self)
        else:
            node.elinstr.acceptInterpreter(self)