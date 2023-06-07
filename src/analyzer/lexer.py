from ply import lex

# List of token names.   This is always required
tokens = (
    'ARROW',
    'ID'
    'MINUS',
    'VALUE'
)

# Regular expression rules for simple tokens
t_ignore = ' \t'

t_ARROW = r'->'
t_MINUS = r'-'


def t_ID(t):

    return t.replace('"', '').replace("'", '')


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Build the lexer
lexer = lex.lex()
