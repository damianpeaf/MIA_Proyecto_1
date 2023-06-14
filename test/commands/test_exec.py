from commands import CommandProxy, Logger


def test_exec():
    Logger.clear_logs()
    print('\ntesting exec command...\n')

    proxy = CommandProxy()
    proxy.reset()

    proxy.execute('configure', {
        'type': 'local',
        'encrypt_log': 'false',
        'encrypt_read': 'true',
        'llave': '1234567890123456',
    })

    # ! no config
    proxy.execute('exec', {
        'path': '/prueba/prueba1.mia',
    })

    Logger.print_logs()
    Logger.clear_logs()
