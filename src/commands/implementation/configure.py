from .common_validators import is_enviroment, is_bool, get_boolean, get_enviroment
from ..strategy import CommandStrategy
from ..config import CommandConfig
from ..logger import OperationType

configure_validations = [
    {
        'param_name': 'type',
        'obligatory': True,
        'validator': lambda t: is_enviroment(t),
    },
    {
        'param_name': 'encrypt_log',
        'obligatory': True,
        'validator': lambda e: is_bool(e),
    },
    {
        'param_name': 'encrypt_read',
        'obligatory': True,
        'validator': lambda e: is_bool(e),
    },
    {
        'param_name': 'llave',
        'obligatory': False,
        'validator': lambda e: True,
    }
]


class ConfigureCommand(CommandStrategy):

    def __init__(self, args: dict[str, str]):
        super().__init__("configure", args, configure_validations)

    def execute(self):

        # Params
        args = self.args
        encrypt_log = get_boolean(args['encrypt_log'])
        encrypt_read = get_boolean(args['encrypt_read'])
        enviroment_type = get_enviroment(args['type'])
        encryption_key = args['llave']

        # Runtime validations
        # if encrypt_log is true or encrypt_read is true, llave is obligatory
        if (encrypt_log or encrypt_read) and (encryption_key is None):
            self.add_error(
                "Si se especifica como 'true' alguno de los parametros 'encrypt_log' o 'encrypt_read', se debe proveer una llave de encriptacion 'llave'",
                OperationType.INPUT
            )
            return False

        self.set_config(CommandConfig(
            enviroment_type,
            encrypt_log,
            encrypt_read,
            encryption_key
        ))

        self.success('Configuracion guardada con exito')
        return True
