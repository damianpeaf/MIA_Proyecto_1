from commands import CommandProxy, Logger


def test_delete():
    try:
        Logger.clear_logs()
        print('\ntesting delete command...\n')

        proxy = CommandProxy()
        proxy.reset()

        # ! no config
        print('\n------ No config ------')
        proxy.execute('delete', {
            'path': '/carpeta1',
            'name': 'prueba1.txt'

        })

        Logger.print_logs()
        Logger.clear_logs()

        # initial config
        proxy.execute('configure', {
            'type': 'cloud',
            'encrypt_log': 'false',
            'encrypt_read': 'false',
        })

        # * CLOUD ENVIRONMENT

        print('\n------ Delete prueba1.txt on /carpeta1/ ------')

        # create file
        # proxy.execute('create', {
        #     'name': 'prueba1.txt',
        #     'path': '/carpeta1/',
        #     'body': 'hola mundo'
        # })

        # proxy.execute('delete', {
        #     'name': 'prueba1.txt',
        #     'path': '/carpeta1/',
        # })

        Logger.print_logs()
        Logger.clear_logs()

        # print('\n------ Delete /carpeta1/ folder ------')
        # # create file
        # # proxy.execute('create', {
        # #     'name': 'prueba1.txt',
        # #     'path': '/carpeta1/',
        # #     'body': 'hola mundo'
        # # })

        proxy.execute('delete', {
            'path': '/carpeta1/',
        })

        Logger.print_logs()
        Logger.clear_logs()

        assert True
    except Exception as e:
        print(e)
        assert False
