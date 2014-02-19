
class Node(object):     
     def __init__(self, type, lineno, children = None, leaf = None):
          self.type = type
          self.lineno = lineno
          if children:
                    self.children = children
          else:
                    self.children = [ ]
          self.leaf = leaf

     def accept(self, visitor):
          className = self.__class__.__name__
          #print "className: ", className
          # return visitor.visit_<className>(self)
          meth = getattr(visitor, 'visit_' + className, None)
          if meth!=None: 
               return meth(self)
          else: 
               print "nie istnieje funkcja ", 'visit_' + className
               return None

     def line(self):
          return self.lineno


class Const(Node):
     def __init__(self, value, typ, lineno):
          Node.__init__(self, "const", lineno)
          self.value = value
          self.type = typ
          self.lineno = lineno


class Integer(Const):
     def __init__(self, value, lineno):
          Const.__init__(self, value, "INTEGER", lineno)
          self.value = value
     #     print "INTEGER"
     #     print lineno
          self.lineno = lineno

class Float(Const):
     def __init__(self, value, lineno):
          Const.__init__(self, value, "FLOAT", lineno)
     #     print "FLOAT"
     #     print lineno
          self.lineno = lineno


class String(Const):
     def __init__(self, value, lineno):
          Const(value, "STRING", lineno)
          self.lineno = lineno


class Variable(Node):
     def __init__(self, typ, variables, lineno):
          Node.__init__(self, "var", lineno)
          self.type = 'var'
          self.typ = typ
          self.variables = variables
          self.lineno = lineno


class BinExpr(Node):
     def __init__(self, left, op, right, lineno):
          Node.__init__(self, "binexpr", lineno)
          self.type = 'binexpr'
          self.left = left
          self.right = right
          self.op = op
          self.lineno = lineno


class RelExpr(Node):
     def __init__(self, left, op, right, lineno):
          Node.__init__(self, "relexpr", lineno)
          self.type = 'relexpr'
          self.left = left
          self.right = right
          self.op = op
          self.lineno = lineno

class Declaration(Node):
     def __init__(self, left, op, right, lineno):
          Node.__init__(self, "decl", lineno)
          self.type = 'decl'
          self.left = left
          self.right = right
          self.op = op
          self.lineno = lineno
          
class Assignment(Node):
     def __init__(self, left, op, right, lineno):
          Node.__init__(self, "=", lineno)
          self.type = '='
          self.left = left
          self.right = right
          self.op = op
          self.lineno = lineno
          
class ChoiceInstruction(Node):
     def __init__(self, cond, instr, lineno):
          Node.__init__(self, "if", lineno)
          self.type = 'if'
          self.cond = cond
          self.instr = instr
          self.lineno = lineno
          
class ChoiceInstructionWithElse(Node):
     def __init__(self, cond, instr, elinstr, lineno):
          Node.__init__(self, "ifelse", lineno)
          self.type = 'ifelse'
          self.cond = cond
          self.instr = instr
          self.elinstr = elinstr
          self.lineno = lineno
          
class WhileLoop(Node):
     def __init__(self, cond, instr, lineno):
          Node.__init__(self, "while", lineno)
          self.type = 'while'
          self.cond = cond
          self.instr = instr
          self.lineno = lineno

class RepeatUntilLoop(Node):
     def __init__(self, instr, cond, lineno):
          Node.__init__(self, "repeat", lineno)
          self.type = 'repeat'
          self.cond = cond
          self.instr = instr
          self.lineno = lineno
          
class Return(Node):
     def __init__(self, value, lineno):
          Node.__init__(self, "return", lineno)
          self.type = 'return'
          self.value = value
          self.lineno = lineno
          
class Break(Node):
     def __init__(self, lineno):
          Node.__init__(self, "break", lineno)
          self.type = 'break'
          self.lineno = lineno
          
class Continue(Node):
     def __init__(self, lineno):
          Node.__init__(self, "continue", lineno)
          self.type = 'continue'
          self.lineno = lineno
          
class Print(Node):
     def __init__(self, expr, lineno):
          Node.__init__(self, "print", lineno)
          self.type = 'print'
          self.expr = expr
          self.lineno = lineno
          
class FunctionDefinition(Node):
     def __init__(self, typ, ident, args, instr, lineno):
          Node.__init__(self, "fundef", lineno)
          self.type = 'fundef'
          self.typ = typ
          self.ident = ident
          self.args = args
          self.instr = instr
          self.lineno = lineno

class FunctionCall(Node):
     def __init__(self, ident, args, lineno):
          Node.__init__(self, "funcall", lineno)
          self.type = 'funcall'
          self.ident = ident
          self.args = args
          self.lineno = lineno
          
class Argument(Node):
     def __init__(self, typ, ident, lineno):
          Node.__init__(self, "arg", lineno)          
          self.type = 'arg'
          self.typ = typ
          self.ident = ident
          self.lineno = lineno
          
class CompoundInstruction(Node):
     def __init__(self, decl, instr, lineno):
          Node.__init__(self, "comp", lineno)
          self.type = 'comp'
          self.decl = decl
          self.instr = instr
          self.lineno = lineno
          
class Label(Node):
     def __init__(self, ident, instr, lineno):
          Node.__init__(self, "label", lineno)
          self.type = 'label'
          self.ident = ident
          self.instr = instr
          self.lineno = lineno
          
class Program(Node):
     def __init__(self, decl, fundef, instr, lineno):
          Node.__init__(self, "program", [decl, fundef, instr], lineno)
          self.type = 'program'
          self.decl = decl
          self.fundef = fundef
          self.instr = instr
          self.lineno = lineno

# ...

def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator
