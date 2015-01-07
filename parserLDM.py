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
    p[0] = AST.AssignNode([AST.IdNumNode(p[3]), p[1]])
def p_instruction_assign_str(p):
    """instruction : chaines ASSIGN_OP IDENTIFIANT_STR ENDL """
    p[0] = AST.AssignNode([AST.IdStrNode(p[3]), p[1]])

def p_instruction_print(p):
    """instruction : PRINT EXPR_START expression EXPR_END ENDL
     |  PRINT EXPR_START chaines EXPR_END ENDL """
    p[0] = AST.PrintNode(p[3])

def p_instruction_while(p):
    """instruction : WHILE EXPR_START condition EXPR_END bloc"""
    p[0] = AST.WhileNode([p[3], p[5]])

def p_expression_token(p):
    """expression : NUMBER"""
    p[0] = AST.NumNode(p[1])

def p_expression_token_id_num(p):
    """expression : IDENTIFIANT """
    p[0] = AST.IdNumNode(p[1])

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

def p_condition(p):
    """condition : expression """
    p[0] = AST.CondNode(p[1])

def p_if(p):
    """instruction : IF EXPR_START condition EXPR_END IF_FALSE bloc IF_TRUE bloc
     | IF EXPR_START condition EXPR_END IF_FALSE bloc """
    try:
        p[0] = AST.IfNode([p[3], p[6], p[8]])
    except:
        p[0] = AST.IfNode([p[3], p[6]])
def p_for(p):
    """instruction : FOR EXPR_START IDENTIFIANT FOR_SEP expression FOR_SEP expression EXPR_END bloc """
    p[0] = AST.ForNode([AST.IdNumNode(p[3]), p[5], p[7], p[9]])


def p_chaine(p):
    """chaine : STR"""
    p[0] = AST.StringNode(p[1])

def p_chaines_str(p):
    """chaines : IDENTIFIANT_STR"""
    p[0] = AST.IdStrNode(p[1])

def p_chaines(p):
    """chaines : chaine
     | expression
     | chaines STR_CONCAT chaines """
    try:
        if isinstance(p[1], AST.StringGroupNode):
            gauche = p[1].children
        else:
            gauche = [p[1]]

        if isinstance(p[3], AST.StringGroupNode):
            droite = p[3].children
        else:
            droite = [p[3]]

        p[0] = AST.StringGroupNode(gauche + droite)

    except:
        p[0] = p[1]

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

def parseFile(file, generateTree = False):
    import tools
    prog = tools.getFileContent(file)
    ast = yacc.parse(prog, debug=0)
    if generateTree:
        name = tools.changeExtension(file, "pdf")
        graph = ast.makegraphicaltree()
        try:
            import os
            os.remove(name)
        except:
            pass
        graph.write_pdf(name)
        return [ast, name]
    else:
        pass
    return [ast, None]

if __name__ == "__main__":
    import tools
    name = tools.getFileNameFromArg("test1.txt")
    result, name = parseFile(name, True)
    print("Wrote ast to " , name)