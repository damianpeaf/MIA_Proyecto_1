from .config import CommandConfig
from .factory import CommandFactory
from .logger import Logger, OperationType
from .implementation import ConfigureCommand


class CommandProxy:

    command_config: CommandConfig = None

    def __init__(self):
        self._factory = CommandFactory()

    def execute(self, command_name: str, args: dict[str, str]):
        command = self._factory.get_command(command_name, args, CommandProxy.command_config)

        # Command related validations
        if command is None:
            Logger.error(f"Commando '{command_name}' no encontrado", OperationType.INPUT)
            return False

        if (CommandProxy.command_config is None) and (not isinstance(command, ConfigureCommand)):
            Logger.error(f"El comando '{command_name}' requiere configuración inicial para ejecutarse", OperationType.INPUT)
            return False

        # Parameters related validations
        if not command.validate_params():
            return False

        # Execute command
        return command.execute()
