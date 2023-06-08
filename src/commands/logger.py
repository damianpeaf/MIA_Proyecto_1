from datetime import datetime
from enum import Enum, auto

from .config import CommandEnvironment


class OperationType(Enum):
    INPUT = auto()
    OUTPUT = auto()


class Logger:

    log_messages = []

    @staticmethod
    def info(message: str, operation_type: OperationType = OperationType.OUTPUT):
        Logger._add_log(message, 'info', operation_type)

    @staticmethod
    def error(message: str, operation_type: OperationType = OperationType.OUTPUT):
        Logger._add_log(message, 'error', operation_type)

    @staticmethod
    def warning(message: str, operation_type: OperationType = OperationType.OUTPUT):
        Logger._add_log(message, 'warning', operation_type)

    @staticmethod
    def success(message: str, operation_type: OperationType = OperationType.OUTPUT):
        Logger._add_log(message, 'success', operation_type)

    @staticmethod
    def _add_log(message: str, type: str, operation_type: OperationType):
        from .proxy import CommandProxy

        enviroment = None

        if CommandProxy.command_config is not None:
            enviroment = 'local' if CommandProxy.command_config.environment == CommandEnvironment.LOCAL else 'cloud'

        Logger.log_messages.append({
            'type': type,
            'message': message,
            'operation_type': 'input' if operation_type == OperationType.INPUT else 'output',
            'date': datetime.now(),
            'enviroment': enviroment
        })

    @staticmethod
    def print_logs():
        for log in Logger.log_messages:
            print(f"[{log['date']}] - {log['operation_type'].upper()} - {log['type'].upper()} - {log['message']} - {log['enviroment']}")

    @staticmethod
    def clear_logs():
        Logger.log_messages = []
