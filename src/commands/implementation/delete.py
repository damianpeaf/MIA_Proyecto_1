from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

delete_validations = [
    {

    }
]


class DeleteCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], config: CommandConfig):
        super().__init__("delete", args, config, delete_validations)

    def execute(self):
        if self.config.environment == CommandEnvironment.CLOUD:
            pass
        elif self.config.environment == CommandEnvironment.LOCAL:
            pass

        return True
