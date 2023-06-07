from analyzer.lexer import lexer

lexer.input("rename -path->/carpeta1/prueba1.txt -name->b1.txt")

while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)


# if __name__ == '__main__':
#     pass
