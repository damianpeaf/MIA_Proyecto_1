from commands import CommandProxy, Logger


def test_modify():
    try:
        Logger.clear_logs()
        print('\ntesting modify command...\n')

        proxy = CommandProxy()
        proxy.reset()

        # ! no config
        print('\n------ No config ------')
        proxy.execute('modify', {
            'path': '/carpeta1/prueba1.txt',
            'body': 'hola mundo'
        })

        Logger.print_logs()
        Logger.clear_logs()

        proxy.execute('configure', {
            'type': 'local',
            'encrypt_log': 'false',
            'encrypt_read': 'false',
        })

        # ! no path
        print('\n------ No path ------')
        proxy.execute('modify', {
            'body': 'hola mundo'
        })

        Logger.print_logs()
        Logger.clear_logs()

        # path not found
        print('\n------ Path not found ------')
        proxy.execute('modify', {
            'path': '/carpeta1/prueba1.txt',
            'body': 'hola mundo'
        })

        Logger.print_logs()
        Logger.clear_logs()

        # ! no body
        print('\n------ No body ------')
        proxy.execute('modify', {
            'path': '/carpeta1/prueba1.txt',
        })

        Logger.print_logs()
        Logger.clear_logs()

        # ! success local

        print('\n------ Success local ------')

        proxy.execute('modify', {
            'path': '/carpeta 2/prueba2.txt',
            'body': 'contenido cambiado para prueba2.txt'
        })

        Logger.print_logs()
        Logger.clear_logs()

        # ! success cloud

        print('\n------ Success cloud ------')

        proxy.execute('configure', {
            'type': 'cloud',
            'encrypt_log': 'false',
            'encrypt_read': 'false',
        })

        proxy.execute('modify', {
            'path': '/sub1/prueba1.txt',
            'body': 'Comando modify ejecutado con exito.'
        })

        Logger.print_logs()
        Logger.clear_logs()

        assert True
    except Exception as e:
        print(e)
        assert False
