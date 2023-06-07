from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

rename_validations = [
    {

    }
]


class RenameCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], config: CommandConfig):
        super().__init__("rename", args, config, rename_validations)

    def execute(self):
        if self.config.environment == CommandEnvironment.CLOUD:
            pass
        elif self.config.environment == CommandEnvironment.LOCAL:
            pass

        return True
