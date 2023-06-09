from .common_validators import is_path
from ..strategy import CommandStrategy
from ..config import CommandEnvironment
from ..logger import OperationType

rename_validations = [
    {
        'param_name': 'path',
        'obligatory': True,
        'validator': lambda p: is_path(p),
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

    def execute(self) -> bool:

        # Params
        args = self.args
        current_path = args['path']
        new_name = args['name']

        alternative_msg = None
        status = True

        if self.get_config().environment == CommandEnvironment.CLOUD:
            resp: bool = self._cloud_service.rename_file_dir(
                current_path, new_name)
            return True
        elif self.get_config().environment == CommandEnvironment.LOCAL:

            resp: bool = self._local_service.rename_file_dir(
                current_path, new_name)

            alternative_msg = resp['msg']
            status = resp['ok']

        if alternative_msg and status:
            self.success(alternative_msg)
            return True
        elif alternative_msg and not status:
            self.add_error(alternative_msg)
            return False
