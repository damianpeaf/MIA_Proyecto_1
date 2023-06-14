from ply import lex

states: tuple[tuple[str, str], ...] = (
    ('valueState', 'exclusive'),
)

# List of token names.   This is always required

tokens: tuple[str, ...] = (
    'ARROW',
    'COMMAND',
    'PARAM',
    'VALUE',
)


# Regular expression rules for simple tokens

t_INITIAL_COMMAND = r'[a-zA-Z]+'
t_PARAM = r'-[a-zA-Z_]+'

# Get value for params


def t_valueState(t):
    r'->'
    t.type = 'ARROW'
    t.lexer.begin('valueState')
    return t


def t_valueState_QUOTED_VALUE(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remove the double quotes
    t.type = 'VALUE'
    t.lexer.begin('INITIAL')
    return t


def t_valueState_VALUE(t):
    r'[^-]+'
    t.value = t.value.strip().replace('"', '')
    t.type = 'VALUE'
    return t


def t_valueState_end(t):
    r'-[a-zA-Z_]+'
    t.type = 'PARAM'
    t.lexer.begin('INITIAL')
    return t


def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0] + " at line " + str(t.lineno) + " at position " + str(t.lexpos))
    t.lexer.skip(1)


def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ANY_ignore = ' \t'


# Build the lexer
lexer = lex.lex()
