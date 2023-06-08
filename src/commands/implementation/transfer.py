from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

transfer_validations = [
    {

    }
]


class TransferCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], config: CommandConfig):
        super().__init__("transfer", args, config, transfer_validations)

    def execute(self):
        if self.config.environment == CommandEnvironment.CLOUD:
            pass
        elif self.config.environment == CommandEnvironment.LOCAL:
            pass

        return True
