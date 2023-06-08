from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

modify_validations = [
    {

    }
]


class ModifyCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], config: CommandConfig):
        super().__init__("modify", args, config, modify_validations)

    def execute(self):
        if self.config.environment == CommandEnvironment.CLOUD:
            pass
        elif self.config.environment == CommandEnvironment.LOCAL:
            pass

        return True
