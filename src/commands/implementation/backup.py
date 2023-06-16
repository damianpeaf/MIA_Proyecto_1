from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment

backup_validations = []


class BackupCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("backup", args,  backup_validations)

    def execute(self):

        resp = None

        if self.get_config().environment == CommandEnvironment.CLOUD:
            # save all files from the cloud to the local
            resp = self._cloud_service.local_backup(self._local_service)
        elif self.get_config().environment == CommandEnvironment.LOCAL:
            # save all files from the local to the cloud
            resp = self._local_service.cloud_backup(self._cloud_service)

        warnings = resp.get('warnings')

        if warnings:
            for warning in warnings:
                self.warning(warning)

        if resp.get('ok'):
            self.success(resp.get('msg'))
        else:
            self.error(resp.get('msg'))

        return True
