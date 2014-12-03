import ply.yacc as yacc
from lex import tokens
import AST


variabes = {}

#def p_programme_statement(p):
#    """programme : statement ENDL"""
#    p[0] = AST.ProgramNode(p[1])
#
#
#def p_programme_recursive(p):
#    """programme : statement ENDL programme """
#    p[0] = AST.ProgramNode([p[1]] + p[3].children)

def p_programme_statement(p):
    """programme : statement ENDL
    | statement ENDL programme"""
    try:
        p[0] = AST.ProgramNode([p[1]] + p[3].children)
    except:
        p[0] = AST.ProgramNode(p[1])


def p_statement(p):
    """statement : affectation
    | structure
    | PRINT expression"""
    try:
        p[0] = AST.PrintNode(p[2])
    except:
        p[0] = p[1]


def p_structure(p):
    """structure : WHILE expression '{' programme '}'"""
    p[0] = AST.WhileNode([p[2], p[4]])


def p_affectation(p):
    """affectation : IDENTIFIANT EQUAL_OP expression """
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_expression_num(p):
    """expression : NUMBER
    | IDENTIFIANT """
    p[0] = AST.TokenNode(p[1])


def p_expression_par(p):
    """expression : "(" expression ")" """
    p[0] = p[2]


operations = {
    '+': lambda x, y: x+y,
    '-': lambda x, y: x-y,
    '*': lambda x, y: x*y,
    '/': lambda x, y: x/y,
}


def p_expression_op(p):
    """expression : expression ADD_OP expression
     | expression MULT_OP expression """
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_minus(p):
    """expression : ADD_OP expression %prec UMINUS"""
    p[0] = AST.OpNode(p[1], [p[2]])


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
    prog = open("test5.txt").read()
    result = yacc.parse(prog, debug=0)
    graph = result.makegraphicaltree()
    name = "test5.pdf"
    try:
        import os
        os.remove(name)
    except:
        pass
    graph.write_pdf(name)
    print("Wrote ast to " , name)