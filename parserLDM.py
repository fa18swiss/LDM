import ply.yacc as yacc
from lexLDM import tokens
import AST

def p_programme(p):
    """programme : bloc"""
    p[0] = AST.ProgramNode(p[1])

def p_bloc(p):
    """bloc : BLOC_START instructions BLOC_END """
    p[0] = AST.BlocNode(p[2])

def p_instructions(p):
    """instructions : instruction
     | instruction instructions"""
    try:
        try:
            # 1er essai, si p[2] est une liste
            p[0] = [p[1]] + p[2]
        except:
            # 2e essai, p[2] n'est pas une liste
            p[0] = [p[1]] + [p[2]]
    except:
        #3e essai, p[2] n'existe pas
        p[0] = p[1]

def p_instruction_assign(p):
    """instruction : expression ASSIGN_OP IDENTIFIANT ENDL """
    p[0] = AST.AssignNode([AST.TokenNode(p[3]), p[1]])

def p_instruction_print(p):
    """instruction : PRINT EXPR_START expression EXPR_END ENDL"""
    p[0] = AST.PrintNode(p[3])

def p_instruction_while(p):
    """instruction : WHILE EXPR_START expression EXPR_END bloc"""
    p[0] = AST.WhileNode([p[3], p[5]])

def p_expression_token(p):
    """expression : NUMBER
    | IDENTIFIANT """
    p[0] = AST.TokenNode(p[1])

def p_expression_op(p):
    """expression : expression ADD_OP expression
     | expression MULT_OP expression """
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_expression_par(p):
    """expression : EXPR_START expression EXPR_END """
    p[0] = p[2]

def p_minus(p):
    """expression : ADD_OP expression %prec UMINUS"""
    p[0] = AST.OpNode(p[1], [p[2]])

def p_if(p):
    """ instruction : IF EXPR_START expression EXPR_END IF_FALSE bloc IF_TRUE bloc """
    p[0] = AST.IfNode([p[3], p[6], p[8]])

def p_error(p):
    #print("Syntax error in line %d" % p.lineno)
    print("Syntax error")
    print(p)
    yacc.errok()

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MULT_OP'),
    ('right', 'UMINUS'),
)

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import codecs
    prog = codecs.open("test1.txt", "r", "UTF-8").read()
    result = yacc.parse(prog, debug=0)
    graph = result.makegraphicaltree()
    name = "test1.pdf"
    try:
        import os
        os.remove(name)
    except:
        pass
    graph.write_pdf(name)
    print("Wrote ast to " , name)