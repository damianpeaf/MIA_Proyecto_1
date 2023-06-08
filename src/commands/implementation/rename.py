import os
from .common_validators import path_exists
from ..strategy import CommandStrategy
from ..config import CommandEnvironment
from ..logger import OperationType

rename_validations = [
    {
        'param_name': 'path',
        'obligatory': True,
        'validator': lambda p: path_exists(p),
    },
    {
        'param_name': 'name',
        'obligatory': True,
        'validator': lambda n: True,
    }
]


class RenameCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("rename", args,  rename_validations)

    def execute(self):
        if self.get_config().environment == CommandEnvironment.CLOUD:
            pass
        elif self.get_config().environment == CommandEnvironment.LOCAL:
            # Params
            args = self.args
            path = args['path']
            name = args['name']

            # Get path without file name
            os_path = os.path.dirname(path)

            # Rename file
            new_file_name = os.path.join(os_path, name)

            if path_exists(new_file_name):
                self.add_error(
                    "Ya existe un archivo con el nombre especificado",
                    OperationType.INPUT
                )
                return False

            self.success('Archivo renombrado exitosamente')

        return True
