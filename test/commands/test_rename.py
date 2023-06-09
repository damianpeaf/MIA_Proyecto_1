from commands import CommandProxy, Logger


def test_rename():
    try:
        Logger.clear_logs()
        print('\ntesting rename command...\n')

        proxy = CommandProxy()
        proxy.reset()

        # ! no config
        print('\n------ No config ------')
        proxy.execute('rename', {
            'path': '/carpeta1/prueba1.txt',
            'name': 'b1.txt'
        })

        Logger.print_logs()
        Logger.clear_logs()

        # initial config
        proxy.execute('configure', {
            'type': 'local',
            'encrypt_log': 'false',
            'encrypt_read': 'false',
        })

        # * LOCAL ENVIRONMENT

        print('\n------ Rename prueba1.txt to b1.txt on /carpeta1/ ------')
        proxy.execute('rename', {
            'path': '/carpeta1/prueba1.txt',
            'name': 'b1.txt'
        })

        Logger.print_logs()
        Logger.clear_logs()

        print('\n------ Rename b1.txt to prueba1.txt on /carpeta1/ ------')
        proxy.execute('rename', {
            'path': '/carpeta1/b1.txt',
            'name': 'prueba1.txt'
        })

        Logger.print_logs()
        Logger.clear_logs()

        # * CLOUD ENVIRONMENT

        # initial config
        proxy.reset()
        proxy.execute('configure', {
            'type': 'cloud',
            'encrypt_log': 'false',
            'encrypt_read': 'false',
        })

        print('\n------ Rename prueba1.txt to b1.txt on /carpeta3/carpeta2/carpetita espacio/prueba2.txt ------')
        proxy.execute('rename', {
            'path': '/carpeta3/carpeta2/carpetita espacio/prueba2.txt',
            'name': 'b1.txt'
        })

        Logger.print_logs()
        Logger.clear_logs()

        assert True
    except Exception as e:
        print(e)
        assert False
