from time import time

from utils import aes_decryption
from .common_validators import is_path
from ..strategy import CommandStrategy
from ..config import CommandConfig, CommandEnvironment
from ..logger import OperationType

exec_validations = [
    {
        'param_name': 'path',
        'obligatory': True,
        'validator': lambda x: is_path(x)
    }
]


class ExecCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("exec", args,  exec_validations)

    def execute(self, proxy):

        init_time = time()
        enviroment = CommandEnvironment.LOCAL

        if self.get_config() is None:
            self.warning(f"Comando 'exec' requiere configuración inicial para ejecutarse, utilizando entorno local por defecto", OperationType.INPUT)
            enviroment = self.get_config().environment

        if enviroment == CommandEnvironment.CLOUD:
            resp = self._cloud_service.get_file_content(self.args.get('path'))
        elif enviroment == CommandEnvironment.LOCAL:
            resp = self._local_service.get_file_content(self.args.get('path'))

        if not resp.get('ok'):
            self.add_error(resp.get('error'))
            return False

        from analyzer.parser import parser

        file_content = resp.get('body')
        file_lines: list[str] = [line for line in file_content.split('\n')]
        config_found = False
        commands = []

        line_number = 0
        for file_line in file_lines:

            line_number += 1

            if file_line.strip() == '':
                continue

            entry = ''
            try:

                # parse first line to get config command
                if not config_found:
                    entry = file_line
                    param_name, params = parser.parse(file_line)
                    # if config command is not found, use previous config
                    if (self.get_config() is None) and param_name != 'configure':
                        self.add_error(f"No se ha especificado comando de configuración inicial dentro del archivo ni se ha establecido un previo", OperationType.INPUT)
                        return False
                    elif (self.get_config() is not None) and param_name != 'configure':
                        self.warning(
                            f"No se ha especificado comando de configuración inicial dentro del archivo, se ha utilizado la configuración previa",
                            OperationType.INPUT
                        )
                    elif param_name == 'configure':
                        config_found = True
                        proxy._exec_runtime({
                            'parsed': (param_name, params),
                            'line': file_line
                        })
                        continue

                    # normal command
                    commands.append({
                        'parsed': (param_name, params),
                        'line': file_line
                    })
                    config_found = True
                    continue

                # rest of lines
                if self.get_config() is None:
                    return False

                # check if read is encrypted
                is_read_encrypted = self.get_config().read_encryption
                if not is_read_encrypted:
                    entry = file_line
                    param_name, params = parser.parse(file_line)
                    commands.append({
                        'parsed': (param_name, params),
                        'line': file_line
                    })
                    continue

                # decrypt line
                decryption_key = self.get_config().encryption_key
                entry = "Desencriptando: " + file_line
                decrypted_lines = aes_decryption(decryption_key, file_line)

                for decrypted_line in decrypted_lines.split('\n'):

                    if decrypted_line.strip() == '':
                        continue

                    entry = "Desencriptación completa: " + decrypted_line
                    param_name, params = parser.parse(decrypted_line)

                    commands.append({
                        'parsed': (param_name, params),
                        'line': decrypted_line
                    })

            except Exception as e:
                print(e)
                self.add_error(f"Error al parsear comando '{entry}', linea: {line_number}", OperationType.INPUT)

        for command in commands:
            proxy._exec_runtime(command)

        total_time = time() - init_time
        total_time_str = f"{total_time:.2f} segundos"
        success_message = f"Archivos Procesados:  -CLOUD: 0 -LOCAL: 0 - Tiempo de ejecución: {total_time_str}"

        self.success(success_message)
        proxy.notify_console(success_message)

        return True
