from commands import CommandProxy, Logger
from analyzer.parser import parser

commands = [
    'Configure -type->local -encrypt_log->false -encrypt_read->false',
    'rEnAme -pAth->/"carpeta1"/prueba1.txt -name->b1.txt'
]


def main():
    for command in commands:
        try:
            s = command
        except EOFError:
            break
        if not s:
            continue
        param_name, params = parser.parse(s)
        print(param_name)
        print(params)

        # proxy = CommandProxy()
        # result = proxy.execute(param_name, params)

        # print(Logger.log_messages)

        # print(CommandProxy.command_config)


if __name__ == '__main__':
    main()
