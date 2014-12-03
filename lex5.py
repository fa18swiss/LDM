import ply.lex as lex

reserved_words = (
    'while',
    'print'
)

tokens = ( 
    'NUMBER',
    'ADD_OP',
    'MULT_OP',
    'EQUAL_OP',
    'IDENTIFIANT',
    'ENDL'
) + tuple(map(lambda s : s.upper(), reserved_words))

t_ADD_OP = r'[+-]'
t_MULT_OP = r'[*/]'
t_EQUAL_OP = r'[=]'
t_ENDL = r'[;]'

literals = '(){}'

def t_NUMBER(t):
    r'\d+\.?\d*'
    try:
        t.value = float(t.value)
    except ValueError:
        print ("Lind %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t

def t_IDENTIFIANT(t):
    r'[a-zA-Z_][\w_]*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
lex.lex()
if __name__ == "__main__":
    import sys
    prog = open("test1.txt").read()
    #prog = open(sys.argv[1]).read()
    lex.input(prog)
    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d : %s (%s) " % (tok.lineno, tok.type, tok.value))

