from commands import CommandProxy, Logger


def test_copy():
    try:

        Logger.clear_logs()
        print('\ntesting copy command...\n')

        proxy = CommandProxy()
        proxy.reset()

        # initial config
        proxy.execute('configure', {
            'type': 'local',
            'encrypt_log': 'false',
            'encrypt_read': 'false',
        })

        # * CLOUD ENVIRONMENT

        # Create directories

        print('\n------ create directories ------')

        proxy.execute('create', {
            'name': 'prueba1.txt',
            'path': '/carpeta1',
            'body': 'contenido del archivo'
        })

        proxy.execute('create', {
            'name': 'prueba2.txt',
            'path': '/carpeta2',
            'body': 'contenido del archivo'
        })

        print('\n------ copy prueba1.txt from /carpeta1/ to /carpeta2/ ------')
        proxy.execute('copy', {
            'from': '/carpeta1/prueba1.txt',
            'to': '/carpeta2/'
        })

        Logger.print_logs()
        Logger.clear_logs()

        print('\n------ copy entire /carpeta1 content to /carpeta2 ------')
        proxy.execute('copy', {
            'from': '/carpeta1/',
            'to': '/carpeta2/'
        })

        Logger.print_logs()
        Logger.clear_logs()

        assert True
    except Exception as e:
        print(e)
        assert False
