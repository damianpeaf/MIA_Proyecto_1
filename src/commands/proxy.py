from .observable import Observable
from .config import CommandConfig
from .factory import CommandFactory
from .logger import Logger, OperationType
from .implementation import ConfigureCommand, ExecCommand


class CommandProxy:

    command_config: CommandConfig = None
    console_event = Observable()

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

        result = False

        if not is_exec_command:
            result = command.execute()
        else:
            result = command.execute(self)

        return result

    def _exec_runtime(self, command: dict[str, any]):
        command_name, params = command.get('parsed')
        command_line = command.get('line')

        # notify command execution, for write in console
        self.notify_console(command_line)

        # execute command
        return self.execute(command_name, params)

    def notify_console(self, command_line: str):
        CommandProxy.console_event.notify_observers(command_line)

    def reset_console_event(self):
        CommandProxy.console_event = Observable()

    def reset(self):
        CommandProxy.command_config = None
