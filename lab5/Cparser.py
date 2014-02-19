#!/usr/bin/python
import ply.yacc as yacc
from scanner import Scanner
from AST import *

class Cparser(object):


    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()
        self.tree = None
        self.errors = 0

    tokens = Scanner.tokens



    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print('At end of input')

    
    
    def p_program(self, p):
        """program : declarations fundefs instructions"""
        #print "PROGRAM\n", p[1], p[2]
        self.tree = Program(p[1],p[2],p[3])

    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        #print "p_declarations", len(p), p.stack
        if len(p)==1: p[0] = Declarations()
        elif len(p)==3: p[0] = p[1].addDeclaration(p[2])
            
    def p_declaration(self, p):
        """declaration : TYPE inits ';' 
                       | error ';' """
        if len(p)==4 : p[0] = p[2].setType(p[1])
        else:
            self.errors+=1   
            print "Declaration in line {0} contains errors.".format(p[1].lineno), "\n"
        #print "p in p_declaration", p[0],"?", p[1],"?", p[2],"?", p[3]


    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
#        print "p in p_inits", len(p), "||", p[0],"?", p[1], p.stack, p.stack[1]
        if len(p)==2: p[0] = Declaration(p[1])
        elif len(p)==4: p[0] = p[1].addInit(p[3])

    def p_init(self, p):
        """init : ID '=' expression """
        #print "p in p_init", p[0],"?", p[1], "?",p[2],"?", p[3]
        p[0] = Variable(p[1],p[3])
    
    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p)==2:
            p[0] = InstructionsList().addInstruction(p[1])
        else:
            p[0] = p[1].addInstruction(p[2])
#        print "p_instructions",

    
    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr 
                       | repeat_instr 
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr"""
#        print "p_instruction",p
        p[0] = p[1]
        #print p[1]
    
    def p_print_instr(self, p):
        """print_instr : PRINT expression ';' """
        p[0] = PrintInstruction(p[2])

    def p_print_instr_error(self, p):
        """print_instr : PRINT error ';' """
        self.errors+=1
        print "Error in print statement. Bad expression", "\n"


    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = LabeledInstruction(p[1],p[3])
    
    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = AssignmentInstruction(p[1],p[3])
    
    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction """
#        print "from choice",p[3],p[5],p[6]
        if len(p)==6: p[0] = IfInstruction(p[3],p[5])
        else: p[0] = IfInstruction(p[3],p[5],p[7])

    def p_choice_instr_error(self, p):
        """choice_instr : IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
#        print "from choice",p[3],p[5],p[6]
        self.errors+=1
        print "Error in choice instruction. Bad condition.", "\n"
    
    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction """
        p[0] = WhileInstruction(p[5],p[3])

    def p_while_instr_error(self, p):
        """while_instr : WHILE '(' error ')' instruction """
        self.errors+=1
        print "Error in while loop. Bad condition.", "\n"

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = RepeatInstruction(p[2],p[4])
    
    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = ReturnInstruction(p[2])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = ContinueInstruction()

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = BreakInstruction()
    
    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions '}' """
        p[0] = CodeBlock(p[2], p[3])
    
    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]


    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        if p[1].typeOf == "FLOAT": p[0] =Const(float(p[1].value))
        elif p[1].typeOf == "INTEGER": p[0] =Const(int(p[1].value))
        elif p[1].typeOf == "STRING": p[0] =Const(p[1].value)
        else: print "Not known const name"
    
    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | ID '(' expr_list_or_empty ')' """
        if len(p) == 2: p[0] = p[1]
        elif len(p) == 4: 
            if p[1] == "(": 
                p[0] = p[2] 
            else: 
                p[0] = BinaryExpression(p[1],p[3],p[2])
        elif len(p) == 5: p[0] = FunctionCall(p[1],p[3])
        else: raise "Not valid expression"
#        print "p in p_expression", p[0], p[1], p.slice[1], p.stack
    
    def p_expression_error(self, p):
        """expression : '(' error ')'
                      | ID '(' error ')' """
        self.errors+=1
        if len(p)==4: print "Error in braced expression. Bad expression.", "\n"
        else: print "Error in arguments list. Bad expression.", "\n"

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p)==1: p[0] = ExpressionsList()
        elif len(p)==2: p[0] = p[1]                              
#        print p                              
    
    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
#        print p
        if len(p)==2: p[0] = ExpressionsList(p[1])
        else: p[0] = p[1].addExpression(p[3])
    
    def p_fundefs(self, p):
        """fundefs : fundef fundefs
                   |  """
        if len(p)==1: p[0] = Functions()
        elif len(p)==3: p[0] = p[2].addFunction(p[1])
#        print p[0]
#        print p

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
#        print p
        p[0] = Function(p[1],p[2],p[4],p[6])
    
    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p)==1: p[0] = ArgumentsList()
        elif len(p)==2: p[0] = p[1]
#        print p[0].printTree(0)

    def p_args_list(self, p):
        """args_list : args_list ',' arg 
                     | arg """
        if len(p)==2: p[0] = ArgumentsList().addArgument(p[1])
        elif len(p)==4: p[0] = p[1].addArgument(p[3])

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = Argument(p[1], p[2])
#        print p

    
