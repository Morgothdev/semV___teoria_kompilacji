from AST import *


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def toString(expression, identation):
    if expression.__class__.__name__=="str":
        return ident(identation) + "`"+expression + "\n"
    else: 
        return expression.printTree(identation)

def ident(count):
    return "|   "*count

class TreePrinter:

    @addToClass(Program)
    def printTree(self, identation):
        return "PROGRAM\n"+self.declarations.printTree(1)+self.functions.printTree(1)+self.code.printTree(3)

    @addToClass(Node)
    def printTree(self,identation):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(Const)
    def printTree(self,identation):
        return ident(identation) + "`" + str(self.value) + "\n"

    @addToClass(Variable)
    def printTree(self, identation):
        if self.const != None: 
            return ident(identation) + "`" + self.name + "\n" + self.const.printTree(identation + 1)
        else: 
            return ident(identation) + "`" + self.name + "\n"    

    @addToClass(Declaration)
    def printTree(self, identation):
        return ident(identation) + "`type=" + str(self.typeOf) +"\n"+ "".join(map(lambda i: i.printTree(identation+1), self.inits))

    @addToClass(Declarations)
    def printTree(self, identation):
        if len(self.declarations)>0:
            return ident(identation) + "`declarations\n"+ "".join(map(lambda i: i.printTree(identation +1), self.declarations))
        else:
            return ""

    @addToClass(Function)
    def printTree(self, identation):
        return ident(identation) + "`function\n"+ident(identation+1) +"`name="+self.name + "\n"+ident(identation+1)+"`returnType="+self.returnType \
        +"\n"+self.arguments.printTree(identation+1) +self.body.printTree(identation+1)

    @addToClass(Functions)
    def printTree(self, identation):
        return ident(identation) + "`functionsList\n"+ "".join(map(lambda i: i.printTree(identation +1), self.functions))

    @addToClass(Argument)
    def printTree(self, identation):
        return ident(identation) + "`" + self.name+"("+self.typeOf+")\n"

    @addToClass(ArgumentsList)
    def printTree(self, identation):
        return ident(identation) + "`args\n" + "".join(map(lambda a: a.printTree(identation+1), self.arguments))

    @addToClass(CodeBlock)
    def printTree(self, identation):
        return ident(identation) + "`code_block\n" + self.declarations.printTree(identation+1) + self.instructions.printTree(identation+1)

    @addToClass(PrintInstruction)
    def printTree(self, identation):
        return ident(identation) + "`print\n"+toString(self.expression,identation+1)

    @addToClass(AssignmentInstruction)
    def printTree(self, identation):
        return ident(identation) + "`assign\n"+ident(identation+1) + self.ident + "\n" +toString(self.expression,identation+1)

    @addToClass(ReturnInstruction)
    def printTree(self, identation):
        return ident(identation) + "`return\n"+ toString(self.expression,identation+1)

    @addToClass(ContinueInstruction)
    def printTree(self, identation):
        return ident(identation) + "`continue\n"

    @addToClass(BreakInstruction)
    def printTree(self, identation):
        return ident(identation) + "`break\n"

    @addToClass(RepeatInstruction)
    def printTree(self, identation):
        return ident(identation) + "`repeat\n" + self.instructions.printTree(identation+1) +ident(identation) + "`until\n"+self.condition.printTree(identation+1)

    @addToClass(LabeledInstruction)
    def printTree(self, identation):
        return ident(identation) + "`named instruction\n"+ident(1+identation) + self.ident + "\n" +self.expression.printTree(identation+1)

    @addToClass(WhileInstruction)
    def printTree(self, identation):
        return ident(identation) + "`while\n" +self.condition.printTree(identation+1)+self.instructions.printTree(identation+1)

    @addToClass(FunctionCall)
    def printTree(self, identation):
        return ident(identation) + "`funCall\n"+ident(identation+1) +"`name="+self.name+"\n"+ident(identation+1) +"`args\n"+self.arguments.printTree(identation+1)

    @addToClass(BinaryExpression)
    def printTree(self, identation):
        return ident(identation) + "`"+self.operator+"\n"+ toString(self.left,identation+1)+toString(self.right,identation+1)

    @addToClass(ExpressionsList)
    def printTree(self, identation):
        return reduce(lambda a,b: a+b,map(lambda i: toString(i,identation+1), self.expressions),"")

    @addToClass(IfInstruction)
    def printTree(self, identation):
        elsIstr = ""
        if self.elseInstruction != None: elsIstr = ident(identation) + "ELSE\n"+ self.elseInstruction.printTree(identation+1)
        return ident(identation) + "`IF\n"+toString(self.test,identation+1)+ident(identation) + "`THEN\n" + self.instruction.printTree(identation+1) + elsIstr

    @addToClass(InstructionsList)
    def printTree(self, identation):
        return ident(identation) + "`insts\n"+reduce(lambda a, b: a+b, map(lambda i: toString(i,identation+1), self.instructions) ,"")