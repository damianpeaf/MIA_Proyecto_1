from ..strategy import CommandStrategy
from ..config import CommandEnvironment
from .common_validators import is_path
from ..logger import OperationType


create_validations = [
    {
        "param_name": "name",
        "obligatory": True,
        "validator": lambda x: True  # ? name.extension
    },
    {
        "param_name": "body",
        "obligatory": True,
        "validator": lambda x: True
    },
    {
        "param_name": "path",
        "obligatory": True,
        "validator": lambda x: is_path(x)
    }
]


class CreateCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("create", args,  create_validations)

    def execute(self):

        # Params
        name = self.args['name']
        body = self.args['body']
        path = self.args['path']

        alternative_msg = None
        status = True

        if self.get_config().environment == CommandEnvironment.CLOUD:
            resp = self._cloud_service.create_file(name, body, path)

            if resp:
                alternative_msg = resp['msg']
                status = resp['ok']

        elif self.get_config().environment == CommandEnvironment.LOCAL:
            resp = self._local_service.create_file(name, body, path)

            alternative_msg = resp['msg']
            status = resp['ok']

        if alternative_msg and status:
            self.success(alternative_msg)
            return True
        elif alternative_msg and not status:
            self.add_error(alternative_msg)
            return False

        self.success(f"Archivo '{name}' creado con exito en la ruta '{path}'")

        return True
