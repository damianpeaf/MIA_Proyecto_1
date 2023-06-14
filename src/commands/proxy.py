from analyzer.parser import parser  # ! <-- Posible circular import
from .config import CommandConfig
from .factory import CommandFactory
from .logger import Logger, OperationType
from .implementation import ConfigureCommand, ExecCommand


class CommandProxy:

    command_config: CommandConfig = None

    def __init__(self):
        self._factory = CommandFactory()

    def execute(self, command_name: str, args: dict[str, str]):
        command = self._factory.get_command(command_name, args)

        # Command related validations
        if command is None:
            Logger.error(f"Comando '{command_name}' no encontrado", OperationType.INPUT)
            return False

        is_config_command = isinstance(command, ConfigureCommand)
        is_exec_command = isinstance(command, ExecCommand)

        if (CommandProxy.command_config is None) and (not (is_config_command or is_exec_command)):
            Logger.error(f"Comando '{command_name}' requiere configuración inicial para ejecutarse", OperationType.INPUT)
            return False

        # Parameters related validations
        if not command.validate_params():
            return False

        # Execute command
        command.info()  # register command execution
        result = command.execute()

        if is_exec_command:
            self._exec_runtime(result)

        return result

    def _exec_runtime(self, commands: list[str]):

        line = 0
        for command in commands:

            line += 1

            if command == '':
                continue

            try:
                # TODO: encrypt read
                param_name, params = parser.parse(command)  # ? error handling ?
                self.execute(param_name, params)
            except:
                Logger.error(f"Error al parsear comando '{command}', linea: {line}", OperationType.INPUT)

    def reset(self):
        CommandProxy.command_config = None
