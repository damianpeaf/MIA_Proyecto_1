from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

delete_validations = [
    {

    }
]


class DeleteCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("delete", args,  delete_validations)

    def execute(self):
        if self.get_config().environment == CommandEnvironment.CLOUD:
            pass
        elif self.get_config().environment == CommandEnvironment.LOCAL:
            pass

        return True
