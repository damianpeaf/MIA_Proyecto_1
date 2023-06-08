from commands import CommandProxy
from analyzer.parser import parser


def main():
    while True:
        try:
            s = 'rEnAme -pAth->/carpeta1/prueba1.txt -name->b1.txt'
        except EOFError:
            break
        if not s:
            continue
        return parser.parse(s)


if __name__ == '__main__':
    param_name, params = main()

    proxy = CommandProxy()
    proxy.execute(param_name, params)
