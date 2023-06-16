from commands import CommandProxy, Logger


def test_transfer():
    return
    try:

        Logger.clear_logs()
        print('\ntesting transfer command...\n')

        proxy = CommandProxy()
        proxy.reset()

        # initial config
        proxy.execute('configure', {
            'type': 'local',
            'encrypt_log': 'false',
            'encrypt_read': 'false',
        })

        # * LOCAL ENVIRONMENT

        # Create directories

        print('\n------ create directories ------')

        # proxy.execute('create', {
        #     'name': 'prueba1.txt',
        #     'path': '/carpeta1',
        #     'body': 'contenido del archivo'
        # })

        # proxy.execute('create', {
        #     'name': 'prueba2.txt',
        #     'path': '/carpeta2',
        #     'body': 'contenido del archivo'
        # })

        # print('\n------ transfer prueba1.txt from /carpeta1/ to /carpeta2/ ------')
        # proxy.execute('transfer', {
        #     'from': '/carpeta1/prueba1.txt',
        #     'to': '/carpeta2/',
        #     'mode': 'local'
        # })

        # Logger.print_logs()
        # Logger.clear_logs()

        print('\n------ transfer entire /carpeta1 content to /carpeta2 ------')
        proxy.execute('transfer', {
            'from': '/carpeta1/',
            'to': '/carpeta2/',
            'mode': 'local'
        })

        Logger.print_logs()
        Logger.clear_logs()

        assert True
    except Exception as e:
        print(e)
        assert False


def test_transfer_cloud():
    try:

        Logger.clear_logs()
        print('\ntesting transfer command for cloud...\n')

        proxy = CommandProxy()
        proxy.reset()

        # initial config
        proxy.execute('configure', {
            'type': 'cloud',
            'encrypt_log': 'falsE',
            'encrypt_read': 'false',
            'llave': '1234678901234567'
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
            'name': 'hola.txt',
            'path': '/carpeta1/subcarpeta1',
            'body': 'hola'
        })

        proxy.execute('create', {
            'name': 'prueba2.txt',
            'path': '/carpeta2',
            'body': 'contenido del archivo'
        })

        # print('\n------ transfer prueba1.txt from /carpeta1/ to /carpeta2/ ------')
        # proxy.execute('transfer', {
        #     'from': '/carpeta1/prueba1.txt',
        #     'to': '/carpeta2/',
        #     'mode': 'cloud'
        # })

        # Logger.print_logs()
        # Logger.clear_logs()

        print('\n------ transfer entire /carpeta1 content to /carpeta2 ------')
        proxy.execute('transfer', {
            'from': '/carpeta1/',
            'to': '/carpeta2/',
            'mode': 'cloud'
        })

        Logger.print_logs()
        Logger.clear_logs()

        assert True
    except Exception as e:
        print(e)
        assert False
