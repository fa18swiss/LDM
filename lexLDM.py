#-*- coding: utf-8 -*-
import ply.lex as lex

tokens = (
    'BLOC_START',
    'BLOC_END',
    'EXPR_START',
    'EXPR_END',
    'NUMBER',
    'ADD_OP',
    'MULT_OP',
    'ASSIGN_OP',
    'IDENTIFIANT',
    'IDENTIFIANT_STR',
    'WHILE',
    'PRINT',
    'IF',
    'IF_FALSE',
    'IF_TRUE',
    'FOR',
    'FOR_SEP',
    'STR',
    'STR_CONCAT',
    'ENDL'
)

t_BLOC_START = r'\]'
t_BLOC_END = r'\('
t_EXPR_START = r'\}'
t_EXPR_END = r'\['
t_ADD_OP = r'[¬§]'
t_MULT_OP = r'[\\¦]'
t_ASSIGN_OP = r'[~]'
t_ENDL = r'\|'
t_IDENTIFIANT = r'[a-zA-Z_][\w_]*'
t_WHILE = r'à'
t_PRINT = r'£'
t_IF = r'ü'
t_IF_FALSE = r'ö'
t_IF_TRUE = r'ä'
t_FOR = r'é'
t_FOR_SEP = r'è'
t_STR_CONCAT = r'\#'
literals = ''

def t_NUMBER(t):
    r'\d+\.?\d*'
    try:
        t.value = float(t.value)
    except ValueError:
        print ("Lind %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t

def t_IDENTIFIANT_STR(t):
    r'°[a-zA-Z_][\w_]*'
    t.value = t.value[1:]
    return t

def t_STR(t):
    r'€[^@]*@'
    t.value = t.value[1:-1]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)




t_ignore = ' \t\r'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    print(t)
    
lex.lex()
if __name__ == "__main__":
    import tools
    prog = tools.getFileContent(tools.getFileNameFromArg("test1.txt"))
    lex.input(prog)
    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d : %s (%s) " % (tok.lineno, tok.type, tok.value))

