from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

copy_validations = [
    {

    }
]


class CopyCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], config: CommandConfig):
        super().__init__("copy", args, config, copy_validations)

    def execute(self):
        if self.config.environment == CommandEnvironment.CLOUD:
            pass
        elif self.config.environment == CommandEnvironment.LOCAL:
            pass

        return True
