def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

class Node(object):

    def __str__(self):
        return self.printTree(0)

class Program(Node):

    def __init__(self, declarations, functions, code):
        self.declarations = declarations
        self.functions = functions
        self.code = code

#stale - typ + wartosc
class Const(Node):

    def __init__(self, value):
        self.value = value
        #print "const created", value

#zmienna - nazwa + jakas przypisana stala
class Variable(Node):

    def __init__(self, nameOfVariable):
        self.const = None
        self.name = nameOfVariable
        #print "variable created", nameOfVariable

    def __init__(self, nameOfVariable, value):
        self.name = nameOfVariable
        self.const = value
        #print "variable created", nameOfVariable, "value", value

class Declaration(Node):

    def __init__(self):
        self.typeOf = None
        self.inits = []        
        
    def __init__(self, init):
        self.typeOf = None
        self.inits = []        
        self.inits.append(init)
 #       #print self, "creating",init

    def addInit(self, init):
#        #print self, "adding",init
        self.inits.append(init)
        return self;

    def setType(self, typeOf):
        self.typeOf = typeOf
#        #print self, typeOf
        return self


class Declarations(Node):
    
    def __init__(self):
        self.declarations = []

    def addDeclaration(self, declaration):
        self.declarations.append(declaration)
#        #print self, "adding declaration",declaration
        return self;


class Function(Node):

    def __init__(self, returnType, name, argumentsList, body):
        self.returnType = returnType
        self.name = name
        self.arguments = argumentsList
        self.body = body

class Functions(Node):
    
    def __init__(self):
        self.functions = []

    def addFunction(self, function):
        self.functions.append(function)
#        #print self, "adding function",function
        return self;

class Argument(Node):

    def __init__(self, typeOf, name):
        self.typeOf = typeOf
        self.name = name
        #print "argument created",typeOf, name

class ArgumentsList(Node):
    def __init__(self):
        self.arguments = []

    def addArgument(self, argument):
        self.arguments.append(argument)
        return self

class CodeBlock(Node):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions

class InstructionsList(Node):
    def __init__(self):
        self.instructions = []

    def addInstruction(self, instruction):
        self.instructions.append(instruction)
        return self

class Instruction(Node):
    pass    

class PrintInstruction(Instruction):
    def __init__(self, expression):
        self.expression = expression

class AssignmentInstruction(Instruction):
    def __init__(self, ident, expression):
        self.ident = ident
        self.expression = expression

class ReturnInstruction(Instruction):
    def __init__(self, expression):
        self.expression =expression

class ContinueInstruction(Instruction):
    pass

class BreakInstruction(Instruction):
    pass

class LabeledInstruction(Instruction):
    def __init__(self, ident, instruction):
        self.ident = ident
        self.instruction = instruction

class LoopInstruction(Instruction):
    def __init__(self, instructions, condition):
        self.instructions = instructions
        self.condition = condition

class RepeatInstruction(LoopInstruction):
    pass

class WhileInstruction(LoopInstruction):
    pass

class BinaryExpression(Node):

    def __init__(self, leftNode, rightNode, operator):
        self.left = leftNode
        self.right = rightNode
        self.operator = operator
        #print "binary created ", operator, leftNode,rightNode


class FunctionCall(Node):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class ExpressionsList(Node):
    def __init__(self, expression):
        self.expressions = []
        self.expressions.append(expression)

    def addExpression(self, expression):
        self.expressions.append(expression)
        return self

class IfInstruction(Node):
    def __init__(self, test, instruction):
        self.test = test
        self.instruction = instruction
        self.elseInstruction = None
        #print "if created, test:",test,"then",instruction

    def __init__(self, test, instruction, elseInstruction):
        self.test = test
        self.instruction = instruction
        self.elseInstruction = elseInstruction