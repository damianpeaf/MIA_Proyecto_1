from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

create_validations = [
    {

    }
]


class CreateCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], config: CommandConfig):
        super().__init__("create", args, config, create_validations)

    def execute(self):
        if self.config.environment == CommandEnvironment.CLOUD:
            pass
        elif self.config.environment == CommandEnvironment.LOCAL:
            pass

        return True
