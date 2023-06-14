from .common_validators import is_path
from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

exec_validations = [
    {
        'param_name': 'path',
        'obligatory': True,
        'validator': lambda x: is_path(x)
    }
]


class ExecCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("exec", args,  exec_validations)

    def execute(self):

        enviroment = CommandEnvironment.LOCAL

        if self.get_config() is not None:
            enviroment = self.get_config().environment

        if enviroment == CommandEnvironment.CLOUD:
            resp = self._cloud_service.get_file_content(self.args.get('path'))
        elif enviroment == CommandEnvironment.LOCAL:
            resp = self._local_service.get_file_content(self.args.get('path'))

        if not resp.get('ok'):
            self.add_error(resp.get('error'))

        content = resp.get('body')
        commands = [line for line in content.split('\n')]

        return commands
