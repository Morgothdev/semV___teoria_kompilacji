import ply.lex as lex

class Value(object):
  def __init__(self, typeOf, value):
    self.typeOf = typeOf
    self.value  = value

  def __str__(self):
    return self.value+"("+self.typeOf+")"


class Scanner(object):

  def find_tok_column(self, token):
    last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
      last_cr = 0
    return token.lexpos - last_cr

  def build(self):
    self.lexer = lex.lex(object=self)
  def input(self, text):
    self.lexer.input(text)

  def token(self):
    a = self.lexer.token()
    return a


  literals = "{}()<>=;:,+-*/%&|^"


  reserved = {
  'break'   : 'BREAK',
  'continue': 'CONTINUE',
  'if'      : 'IF',
  'else'    : 'ELSE',
  'print'   : 'PRINT',
  'repeat'  : 'REPEAT',
  'return'  : 'RETURN',
  'while'   : 'WHILE',
  'until'   : 'UNTIL',
  }


  tokens = [ "AND", "EQ", "FLOAT", "GE", "ID", "INTEGER", "LE", "NEQ", "OR",
             "SHL", "SHR", "STRING", "TYPE",  ] + list(reserved.values())
           

  t_ignore = ' \t\f'

  def t_newline(self,t):
      r'\n+'
      t.lexer.lineno += len(t.value)

  def t_newline2(self,t):
      r'(\r\n)+'
      t.lexer.lineno += len(t.value) / 2


  def t_error(self,t):
      print("Illegal character '{0}' ({1}) in line {2}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
      t.lexer.skip(1)


  def t_LINE_COMMENT(self,t):
      r'\#.*'
      pass

  def t_BLOCK_COMMENT(self,t):
      r'/\*(.|\n)*?\*/'
      t.lexer.lineno += t.value.count('\n')
      

  def t_FLOAT(self,t):
      r"\d+(\.\d*)|\.\d+"
      t.value = Value("FLOAT",t.value)
      return t

  def t_INTEGER(self,t):
      r"\d+"
      t.value = Value("INTEGER",t.value)
      return t
  
  def t_STRING(self,t):
      r'\"([^\\\n]|(\\.))*?\"'
      t.value = Value("STRING",t.value)
      return t
  
  t_LE = r"<="
    
  t_GE = r">="
  
  t_EQ = r"=="
  
  t_NEQ = r"!="


  def t_TYPE(self,t):
      r"\b(int|float|string)\b"
      #print "t in t_TYPE", t, t.value
      return t
  
  def t_ID(self,t):
      r"[a-zA-Z_]\w*"
      #print "t in t_ID", t, t.value
      t.type = Scanner.reserved.get(t.value, 'ID')
      return t