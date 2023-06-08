from ply.yacc import yacc

from analyzer import lexer

tokens = lexer.tokens

# Example of command to parse: rename -path->/carpeta1/prueba1.txt -name->b1.txt

# Grammar rules and actions
# We must return a tuple like this: ('COMMAND', {
# 'param1': 'value1', 'param2': 'value2', ...})


def p_init(p):
    '''init : COMMAND parameters 
            | COMMAND'''
    if len(p) > 2:
        p[0] = (p[1].lower(), {
            **p[2]
        })
    else:
        p[0] = (p[1], {})


def p_parameters(p):
    '''parameters : parameters parameter 
                | parameter'''
    if len(p) > 2:
        p[0] = {**p[1], **p[2]}
    else:
        p[0] = p[1]


def p_parameter(p):
    'parameter : PARAM ARROW VALUE'
    p[0] = {p[1].lstrip('-').lower(): p[3]}


def p_error(p):
    print(f'Syntax error {p.value!r}, line {p.lineno}')


parser = yacc()
