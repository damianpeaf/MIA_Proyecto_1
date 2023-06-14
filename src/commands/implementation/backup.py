from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

backup_validations = []


class BackupCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("backup", args,  backup_validations)

    def execute(self):
        if self.get_config().environment == CommandEnvironment.CLOUD:
            pass
        elif self.get_config().environment == CommandEnvironment.LOCAL:
            pass

        return True
