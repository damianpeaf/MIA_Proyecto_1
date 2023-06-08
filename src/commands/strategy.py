from typing import Dict, Callable, List
from abc import ABC, abstractmethod

from .config import CommandConfig
from .validator import ParamValidator
from .logger import Logger, OperationType


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

    def __init__(self, command_name: str, args: dict[str, str], config: CommandConfig, validations: List[Dict[str, any]]):
        super().__init__()
        self.command_name = command_name
        self.args = args
        self.config = config
        self._validator = ParamValidator(self.command_name, validations)

        # TODO: Add cloud client
        self._cloud_client = None

    def validate_params(self):
        return self._validator.validate(self.args)

    def add_error(self, error: str, operation_type: OperationType = OperationType.OUTPUT):
        Logger.error(f"En el comando: '{self.command_name}': " + error, operation_type)

    def success(self, message: str = ''):
        Logger.success(f'Comando {self.command_name} ejecutado con exito. {message}', OperationType.OUTPUT)

    @abstractmethod
    def execute(self) -> bool:
        pass
