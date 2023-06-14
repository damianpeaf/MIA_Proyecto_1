from typing import Dict, List
from abc import ABC, abstractmethod

from .service import LocalFileService, CloudFileService
from .config import CommandConfig
from .validator import ParamValidator
from .logger import Logger, OperationType

default_cloud_service = CloudFileService()


class CommandStrategy(ABC):

    """
    validations looks like this:

    [
        {
            "param_name": "param1",
            "obligatory": True,
            "validator": lambda x: x == "value1"
        }
    ]

    """

    def __init__(self, command_name: str, args: dict[str, str], validations: List[Dict[str, any]]):
        super().__init__()
        self.command_name = command_name
        self.args = args
        self._validator = ParamValidator(self.command_name, validations)

        self._cloud_service = default_cloud_service
        self._local_service = LocalFileService()

    def validate_params(self):
        return self._validator.validate(self.args)

    def add_error(self, error: str, operation_type: OperationType = OperationType.OUTPUT):
        Logger.error(f"Comando: '{self.command_name}' - {error}", operation_type)

    def success(self, message: str = ''):
        Logger.success(f'Comando {self.command_name} - {message}', OperationType.OUTPUT)

    def warning(self, message: str = ''):
        Logger.warning(f"Comando '{self.command_name}' - {message}", OperationType.OUTPUT)

    def get_config(self) -> CommandConfig:
        from .proxy import CommandProxy
        return CommandProxy.command_config

    def set_config(self, config: CommandConfig):
        from .proxy import CommandProxy
        CommandProxy.command_config = config

    def info(self):
        formated_args = ', '.join([f"{key}='{value}'" for key, value in self.args.items()])
        Logger.info(f"Comando {self.command_name} - {formated_args} ", OperationType.INPUT)

    @abstractmethod
    def execute(self) -> bool:
        pass
