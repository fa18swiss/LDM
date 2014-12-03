#-*- coding: utf-8 -*-
import ply.lex as lex

tokens = ( 
    'NUMBER',
    'OPERATOR',
    'EQUAL_OP',
    'IDENTIFIANT',
    'ENDL'
)

t_OPERATOR = r'[¬§\\¦]'
t_EQUAL_OP = r'[~]'
t_ENDL = r'\|'
t_IDENTIFIANT = r'[a-zA-Z_][\w_]*'
literals = 'éèà£üöä](}['

def t_NUMBER(t):
    r'\d+\.?\d*'
    try:
        t.value = float(t.value)
    except ValueError:
        print ("Lind %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    print(t)
    
lex.lex()
if __name__ == "__main__":
    import codecs
    prog = codecs.open("test1.txt", "r", "UTF-8").read()
    lex.input(prog)
    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d : %s (%s) " % (tok.lineno, tok.type, tok.value))

