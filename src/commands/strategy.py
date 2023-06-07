from abc import ABC, abstractmethod

from .config import CommandConfig, CommandEnvironment


class CommandStrategy(ABC):

    def __init__(self, operation: str, args: dict[str, str], config: CommandConfig, strategy_type: CommandEnvironment):
        super().__init__()
        self.operation = operation
        self.args = args
        self.config = config
        self.strategy_type: CommandEnvironment = strategy_type

    @abstractmethod
    def validate_params(self):
        pass

    @abstractmethod
    def execute(self):
        pass


class LocalCommandStrategy(CommandStrategy):

    def __init__(self, operation: str, args: dict[str, str], config: CommandConfig):
        super().__init__(operation, args, config, CommandEnvironment.LOCAL)


class CloudCommandStrategy(CommandStrategy):

    def __init__(self, operation: str, args: dict[str, str], config: CommandConfig):
        super().__init__(operation, args, config, CommandEnvironment.CLOUD)

        # TODO: Add cloud client
        self._cloud_client = None
