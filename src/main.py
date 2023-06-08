from commands import CommandProxy, Logger
from analyzer.parser import parser


def main():
    while True:
        try:
            # s = 'rEnAme -pAth->/carpeta1/prueba1.txt -name->b1.txt'
            s = 'Configure -type->local -encrypt_log->false -encrypt_read->false'
        except EOFError:
            break
        if not s:
            continue
        return parser.parse(s)


if __name__ == '__main__':
    param_name, params = main()

    proxy = CommandProxy()
    result = proxy.execute(param_name, params)

    print(Logger.log_messages)

    print(CommandProxy.command_config)
