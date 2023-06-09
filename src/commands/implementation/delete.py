from .common_validators import is_path
from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

delete_validations = [
    {
        "param_name": 'path',
        "obligatory": True,
        "validator": lambda x: is_path(x)
    },
    {
        "param_name": 'name',
        "obligatory": False,
        "validator": lambda x: True
    }
]


class DeleteCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("delete", args,  delete_validations)

    def execute(self):

        path = self.args['path']
        name = self.args['name']

        msg = ''
        status = True

        if self.get_config().environment == CommandEnvironment.CLOUD:
            result = self._cloud_service.delete_resource(path, name)

            msg = result['msg']
            status = result['ok']

        elif self.get_config().environment == CommandEnvironment.LOCAL:
            result = self._local_service.delete_resource(path, name)

            msg = result['msg']
            status = result['ok']

        if status:
            self.success(msg)
            return True

        self.add_error(msg)
        return False
