from datetime import datetime
from enum import Enum, auto
from os import path, makedirs

from utils import aes_encryption
from .config import CommandEnvironment
from .service import LOCAL_ROOT_PATH


class OperationType(Enum):
    INPUT = auto()
    OUTPUT = auto()
    AUTH = auto()


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
        Logger._add_log(message, 'advertencia', operation_type)

    @staticmethod
    def success(message: str, operation_type: OperationType = OperationType.OUTPUT):
        Logger._add_log(message, 'exito', operation_type)

    @staticmethod
    def _add_log(message: str, type: str, operation_type: OperationType):
        from .proxy import CommandProxy

        enviroment = None

        if CommandProxy.command_config is not None:
            enviroment = 'local' if CommandProxy.command_config.environment == CommandEnvironment.LOCAL else 'cloud'

        Logger.log_messages.append({
            'type': type,
            'message': message,
            'operation_type': operation_type.name,
            'date': datetime.now(),
            'enviroment': 'No configurado' if enviroment is None else enviroment
        })

        Logger._write_binnacle()

        CommandProxy.console_event.notify_observers(f"{type} - {message} - Entorno: {'No configurado' if enviroment is None else enviroment}")

    @staticmethod
    def print_logs():
        for log in Logger.log_messages:
            date = log['date'].strftime("%d/%m/%Y %H:%M:%S")
            print(f"[{date}] - {log['operation_type'].upper()} - {log['type'].upper()} - {log['message']} - Entorno: {log['enviroment']}")

    @staticmethod
    def get_log_str(index: int):
        log = Logger.log_messages[index]
        date = log['date'].strftime("%d/%m/%Y %H:%M:%S")
        return f"[{date}] - {log['operation_type'].upper()} - {log['type'].upper()} - {log['message']} - Entorno: {log['enviroment']}"

    @staticmethod
    def clear_logs():
        Logger.log_messages = []

    @staticmethod
    def _write_binnacle():

        year = str(datetime.now().year)
        month = str(datetime.now().month)
        day = str(datetime.now().day)

        binnacle_path = path.join(LOCAL_ROOT_PATH, year, month, day)

        if not path.exists(binnacle_path):
            makedirs(binnacle_path)

        binnacle_file_name = 'log_archivos.txt'

        # create file if not exists
        binnacle_file_path = path.join(binnacle_path, binnacle_file_name)

        if not path.exists(binnacle_file_path):
            open(binnacle_file_path, 'w', encoding='utf-8').close()

        # if exists, append the last log

        # write with format utf-8
        from .proxy import CommandProxy

        with open(binnacle_file_path, 'a', encoding='utf-8') as binnacle_file:

            if CommandProxy.command_config is not None:

                encrypt = CommandProxy.command_config.log_encryption

                if encrypt:
                    encryption_key = CommandProxy.command_config.encryption_key
                    data = aes_encryption(encryption_key, Logger.get_log_str(len(Logger.log_messages) - 1))
                    binnacle_file.write(f"{data}\n")
                    return

            binnacle_file.write(f"{Logger.get_log_str(len(Logger.log_messages) - 1)}\n")
