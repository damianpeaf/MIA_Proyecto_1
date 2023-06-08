from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

configure_validations = [
    {

    }
]


class ConfigureCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], config: CommandConfig):
        super().__init__("configure", args, config, configure_validations)

    def execute(self):
        if self.config.environment == CommandEnvironment.CLOUD:
            pass
        elif self.config.environment == CommandEnvironment.LOCAL:
            pass

        return True
