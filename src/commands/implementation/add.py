from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

add_validations = [
    {

    }
]


class AddCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], config: CommandConfig):
        super().__init__("add", args, config, add_validations)

    def execute(self):
        if self.config.environment == CommandEnvironment.CLOUD:
            pass
        elif self.config.environment == CommandEnvironment.LOCAL:
            pass

        return True
