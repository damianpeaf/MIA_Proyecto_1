from commands import CommandProxy, Logger


def test_backup_cloud():
    try:

        Logger.clear_logs()
        print('\ntesting backup command for cloud...\n')

        proxy = CommandProxy()
        proxy.reset()

        # initial config
        proxy.execute('configure', {
            'type': 'cloud',
            'encrypt_log': 'false',
            'encrypt_read': 'false',
        })

        # * CLOUD ENVIRONMENT

        print('\n------ backup ------')
        proxy.execute('backup', {})

        Logger.print_logs()
        Logger.clear_logs()

        assert True
    except Exception as e:
        print(e)
        assert False
