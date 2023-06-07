from ply import lex

# List of token names.   This is always required

tokens = (
    'ARROW',
    'COMMAND',
    'PARAM',
    'VALUE',
)

# Regular expression rules for simple tokens

t_ARROW = r'->'
t_COMMAND = r'[a-zA-Z]+'
t_PARAM = r'-[a-zA-Z]+'
t_VALUE = r'[^->\s]+'


def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ANY_ignore = ' \t'


# Build the lexer
lexer = lex.lex()
