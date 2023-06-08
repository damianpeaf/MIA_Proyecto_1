from analyzer.parser import parser


def main():
    while True:
        try:
            s = 'rename -path->/carpeta1/prueba1.txt -name->b1.txt'
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)
        break


if __name__ == '__main__':
    main()
