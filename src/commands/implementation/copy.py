from .common_validators import is_path
from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

copy_validations = [
    {
        "param_name": "from",
        "obligatory": True,
        "validator": lambda f: is_path(f)
    },
    {
        "param_name": "to",
        "obligatory": True,
        "validator": lambda f: is_path(f)
    }
]


class CopyCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("copy", args,  copy_validations)

    def execute(self):

        # response
        ok = False
        msg = ''
        warnings = []

        # args
        from_path = self.args['from']
        to_path = self.args['to']

        if self.get_config().environment == CommandEnvironment.CLOUD:
            pass
        elif self.get_config().environment == CommandEnvironment.LOCAL:
            resp = self._local_service.copy_resource(from_path, to_path)

            ok = resp['ok']
            msg = resp['msg']

            if 'warnings' in resp:
                warnings = resp['warnings']

        if ok:
            self.success(msg)
        else:
            self.add_error(msg)

        for warning in warnings:
            self.warning(warning)

        return True
