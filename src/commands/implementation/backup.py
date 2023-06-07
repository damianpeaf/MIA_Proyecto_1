from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

backup_validations = [
    {

    }
]


class BackupCommand(CommandStrategy):

    def __init__(self, args: dict[str, str], config: CommandConfig):
        super().__init__("backup", args, config, backup_validations)

    def execute(self):
        if self.config.environment == CommandEnvironment.CLOUD:
            pass
        elif self.config.environment == CommandEnvironment.LOCAL:
            pass

        return True
