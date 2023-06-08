from datetime import datetime
from enum import Enum, auto


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
        Logger.log_messages.append({
            'type': type,
            'message': message,
            'operation_type': 'input' if operation_type == OperationType.INPUT else 'output',
            'date': datetime.now()
        })
