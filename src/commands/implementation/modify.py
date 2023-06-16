from .common_validators import is_path
from ..strategy import CommandStrategy
from ..config import CommandEnvironment

modify_validations = [
    {
        'param_name': 'path',
        'obligatory': True,
        'validator': lambda p: is_path(p),
    },
    {
        'param_name': 'body',
        'obligatory': True,
        'validator': lambda n: True,
    }
]


class ModifyCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("modify", args,  modify_validations)

    def execute(self):
        # Params
        args = self.args
        current_path = args['path']
        body = args['body']

        alternative_msg = None
        status = True

        if self.get_config().environment == CommandEnvironment.CLOUD:

            response = self._cloud_service.add_content(
                current_path, body, False)

            alternative_msg = response['msg']
            status = response['ok']
        elif self.get_config().environment == CommandEnvironment.LOCAL:

            response = self._local_service.modify_resource(current_path, body)

            alternative_msg = response['msg']
            status = response['ok']

        if alternative_msg and status:
            self.success(alternative_msg)
            return True
        elif alternative_msg and not status:
            self.add_error(alternative_msg)
            return False
