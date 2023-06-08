from .config import CommandConfig

from .implementation import *


class CommandFactory:

    def get_command(command_name: str, args: dict[str, str], config: CommandConfig):

        # ? Make config accssible from command implementations (CommandProxy.command_config)

        if command_name == 'add':
            return AddCommand(args, config)
        elif command_name == 'backup':
            return BackupCommand(args, config)
        elif command_name == 'configure':
            return ConfigureCommand(args, config)
        elif command_name == 'copy':
            return CopyCommand(args, config)
        elif command_name == 'create':
            return CreateCommand(args, config)
        elif command_name == 'delete':
            return DeleteCommand(args, config)
        elif command_name == 'modify':
            return ModifyCommand(args, config)
        elif command_name == 'rename':
            return RenameCommand(args, config)
        elif command_name == 'transfer':
            return TransferCommand(args, config)

        return None
