
class Node(object):     
     def __init__(self, type, lineno):
          self.type = type
          self.lineno = lineno

     def accept(self, visitor):
          className = self.__class__.__name__
          meth = getattr(visitor, 'visit_' + className, None)
          if meth!=None: 
               return meth(self)
          else: 
               print "nie istnieje funkcja ", 'visit_' + className
               return None

     def acceptInterpreter(self, visitor):
          return visitor.visit(self)

     def line(self):
          return self.lineno


class Const(Node):
     def __init__(self, value, typ, lineno):
          Node.__init__(self, "const", lineno)
          self.value = value
          self.type = typ

class Integer(Const):
     def __init__(self, value, lineno):
          Const.__init__(self, int(value), "INTEGER", lineno)

class Float(Const):
     def __init__(self, value, lineno):
          Const.__init__(self, float(value), "FLOAT", lineno)

class String(Const):
     def __init__(self, value, lineno):
          Const.__init__(self, value, "STRING", lineno)

class Variable(Node):
     def __init__(self, typ, variables, lineno):
          Node.__init__(self, "var", lineno)
          self.type = 'var'
          self.typ = typ
          self.variables = variables

class BinExpr(Node):
     def __init__(self, left, op, right, lineno):
          Node.__init__(self, "binexpr", lineno)
          self.type = 'binexpr'
          self.left = left
          self.right = right
          self.op = op

class RelExpr(Node):
     def __init__(self, left, op, right, lineno):
          Node.__init__(self, "relexpr", lineno)
          self.type = 'relexpr'
          self.left = left
          self.right = right
          self.op = op

class Declaration(Node):
     def __init__(self, left, op, right, lineno):
          Node.__init__(self, "decl", lineno)
          self.type = 'decl'
          self.left = left
          self.right = right
          self.op = op
          
class Assignment(Node):
     def __init__(self, left, op, right, lineno):
          Node.__init__(self, "=", lineno)
          self.type = '='
          self.left = left
          self.right = right
          self.op = op
          
class ChoiceInstruction(Node):
     def __init__(self, cond, instr, lineno):
          Node.__init__(self, "if", lineno)
          self.type = 'if'
          self.cond = cond
          self.instr = instr
          
class ChoiceInstructionWithElse(Node):
     def __init__(self, cond, instr, elinstr, lineno):
          Node.__init__(self, "ifelse", lineno)
          self.type = 'ifelse'
          self.cond = cond
          self.instr = instr
          self.elinstr = elinstr
          
class WhileLoop(Node):
     def __init__(self, cond, instr, lineno):
          Node.__init__(self, "while", lineno)
          self.type = 'while'
          self.cond = cond
          self.instr = instr

class RepeatUntilLoop(Node):
     def __init__(self, instr, cond, lineno):
          Node.__init__(self, "repeat", lineno)
          self.type = 'repeat'
          self.cond = cond
          self.instr = instr
          
class Return(Node):
     def __init__(self, value, lineno):
          Node.__init__(self, "return", lineno)
          self.type = 'return'
          self.value = value
          
class Break(Node):
     def __init__(self, lineno):
          Node.__init__(self, "break", lineno)
          self.type = 'break'
          
class Continue(Node):
     def __init__(self, lineno):
          Node.__init__(self, "continue", lineno)
          self.type = 'continue'
          
class Print(Node):
     def __init__(self, expr, lineno):
          Node.__init__(self, "print", lineno)
          self.type = 'print'
          self.expr = expr
          
class FunctionDefinition(Node):
     def __init__(self, typ, ident, args, instr, lineno):
          Node.__init__(self, "fundef", lineno)
          self.type = 'fundef'
          self.typ = typ
          self.ident = ident
          self.args = args
          self.instr = instr

class FunctionCall(Node):
     def __init__(self, ident, args, lineno):
          Node.__init__(self, "funcall", lineno)
          self.type = 'funcall'
          self.ident = ident
          self.args = args
          
class Argument(Node):
     def __init__(self, typ, ident, lineno):
          Node.__init__(self, "arg", lineno)          
          self.type = 'arg'
          self.typ = typ
          self.ident = ident
          
class CompoundInstruction(Node):
     def __init__(self, decl, instr, lineno):
          Node.__init__(self, "comp", lineno)
          self.type = 'comp'
          self.decl = decl
          self.instr = instr
          
class Label(Node):
     def __init__(self, ident, instr, lineno):
          Node.__init__(self, "label", lineno)
          self.type = 'label'
          self.ident = ident
          self.instr = instr
          
class Program(Node):
     def __init__(self, decl, fundef, instr, lineno):
          Node.__init__(self, "program", lineno)
          self.type = 'program'
          self.decl = decl
          self.fundef = fundef
          self.instr = instr

def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator
