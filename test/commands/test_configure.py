from commands import CommandProxy, Logger


def test_configure():
    try:

        print('\ntesting configure command...\n')

        proxy = CommandProxy()

        # Missing params
        print('\n------ Missing params ------')
        proxy.execute('configure', {
            'type': 'local',
            'encrypt_log': 'false',
        })

        Logger.print_logs()
        Logger.clear_logs()

        # Invalid params
        print('\n------ Invalid params ------')
        proxy.execute('configure', {
            'type': 'local',
            'encrypt_log': 'notfalse',
            'encrypt_read': 'notfalse',
            'llave': '1234'
        })

        Logger.print_logs()
        Logger.clear_logs()

        # unnecessary params
        print('\n------ unnecessary params ------')
        proxy.execute('configure', {
            'type': 'local',
            'encrypt_log': 'false',
            'encrypt_read': 'false',
            'llave': '1234',
            'unnecessary': 'param'
        })

        Logger.print_logs()
        Logger.clear_logs()

        # No key provided
        print('\n------ No key provided ------')
        proxy.execute('configure', {
            'type': 'cloud',
            'encrypt_log': 'true',
            'encrypt_read': 'true',
        })

        Logger.print_logs()
        Logger.clear_logs()

        # correct with no key
        print('\n------ Correct with no key ------')
        proxy.execute('configure', {
            'type': 'local',
            'encrypt_log': 'false',
            'encrypt_read': 'false',
        })

        Logger.print_logs()
        print(CommandProxy.command_config)
        Logger.clear_logs()

        # correct with key
        print('\n------ Correct with key ------')
        proxy.execute('configure', {
            'type': 'cloud',
            'encrypt_log': 'true',
            'encrypt_read': 'true',
            'llave': '1234'
        })

        Logger.print_logs()
        print(CommandProxy.command_config)

        # 😋
        assert True

    except:
        assert False
