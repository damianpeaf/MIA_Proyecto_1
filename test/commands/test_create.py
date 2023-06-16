from commands import CommandProxy, Logger


def test_create():
    try:

        Logger.clear_logs()
        print('\ntesting create command...\n')

        proxy = CommandProxy()
        proxy.reset()

        # ! no config
        print('\n------ No config ------')
        proxy.execute('create', {
            'name': 'prueba2.txt',
            'path': '/carpeta 2',
            'body': 'contenido del archivo'
        })

        Logger.print_logs()
        Logger.clear_logs()

        # initial config
        proxy.execute('configure', {
            'type': 'local',
            'encrypt_log': 'false',
            'encrypt_read': 'false',
        })

        # * CLOUD ENVIRONMENT

        print('\n------ Create prueba1.txt on /carpeta1/ ------')
        proxy.execute('create', {
            'name': 'prueba2.txt',
            'path': '/carpeta3/carpeta2/carpetita espacio/',
            'body': 'contenido del archivo'
        })

        Logger.print_logs()
        Logger.clear_logs()

        assert True
    except Exception as e:
        print(e)
        assert False
