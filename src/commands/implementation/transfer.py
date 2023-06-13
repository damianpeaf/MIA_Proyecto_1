from .common_validators import is_path, is_enviroment, get_enviroment
from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

transfer_validations = [
    {
        "param_name": "from",
        "obligatory": True,
        "validator": lambda f: is_path(f)
    },
    {
        "param_name": "to",
        "obligatory": True,
        "validator": lambda f: is_path(f)
    },
    {
        "param_name": "mode",
        "obligatory": True,
        "validator": lambda m: is_enviroment(m)
    }
]


class TransferCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("transfer", args,  transfer_validations)

    def execute(self):

        args = self.args

        from_param = args["from"]
        to_param = args["to"]
        mode_param = get_enviroment(args["mode"])

        # runtime validations

        if mode_param != self.get_config().environment:

            actual_env = 'local' if self.get_config().environment == CommandEnvironment.LOCAL else 'cloud'
            mode_env = 'local' if mode_param == CommandEnvironment.LOCAL else 'cloud'

            self.add_error(
                f"Se ha configurado un modo de transferencia diferente al del entorno actual. Configurado inicialmente: {actual_env}, actual: {mode_env}"
            )
            return False

        resp = None

        if self.get_config().environment == CommandEnvironment.CLOUD:
            resp = self._cloud_service.transfer_resource(from_param, to_param)
        elif self.get_config().environment == CommandEnvironment.LOCAL:
            resp = self._local_service.transfer_resource(from_param, to_param)

        if 'warnings' in resp:
            for warning in resp['warnings']:
                self.warning(warning)

        if resp['ok']:
            self.success(resp['msg'])
        else:
            self.add_error(resp['msg'])
            return False

        return True
