from .config import CommandConfig

from .implementation import *


class CommandFactory:

    def __init__(self):
        pass

    def get_command(self, command_name: str, args: dict[str, str]):

        if command_name == 'add':
            return AddCommand(args)
        elif command_name == 'backup':
            return BackupCommand(args)
        elif command_name == 'configure':
            return ConfigureCommand(args)
        elif command_name == 'copy':
            return CopyCommand(args)
        elif command_name == 'create':
            return CreateCommand(args)
        elif command_name == 'delete':
            return DeleteCommand(args)
        elif command_name == 'modify':
            return ModifyCommand(args)
        elif command_name == 'rename':
            return RenameCommand(args)
        elif command_name == 'transfer':
            return TransferCommand(args)
        elif command_name == 'exec':
            return ExecCommand(args)

        return None
