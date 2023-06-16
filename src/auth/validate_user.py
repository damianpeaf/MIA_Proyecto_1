from os import path

from utils import aes_encryption, aes_decryption
from commands import LOCAL_BASE_PATH, Logger, OperationType

USERS_FILE = 'miausuarios.txt'
AES_KEY = 'miaproyecto12345'

"""
Takes the username and password and validates them against the users.txt file.

Keyword arguments:
username -- The username to validate.|
password -- The password to validate.

Returns:
True if the username and password are valid, False otherwise.
"""


def validate_user(username: str = '', password: str = '') -> bool:

    Logger.info('Intento de inicio de sesión del usuario: ' + username, OperationType.AUTH)

    if not path.exists(path.join(LOCAL_BASE_PATH, USERS_FILE)):
        Logger.error('El archivo de usuarios no existe.', OperationType.AUTH)
        return False

    with open(path.join(LOCAL_BASE_PATH, USERS_FILE), 'r') as users_file:
        lines = users_file.readlines()

        username_found = False
        check = True  # true for username, false for password

        for line in lines:

            # Skip empty lines
            if line.strip() == '':
                continue

            # If the username was found, check the password
            if username_found:
                if line.strip().upper() == aes_encryption(AES_KEY, password).upper():
                    Logger.info('Inicio de sesión exitoso del usuario: ' + username, OperationType.AUTH)
                    return {
                        'username': username,
                        'ok': True
                    }

                # If the password was not found, return False
                Logger.error('Contraseña incorrecta para el usuario: ' + username, OperationType.AUTH)
                return {
                    'username': username,
                    'ok': False
                }
            elif check:
                if line.strip() == username.strip():
                    username_found = True

            check = not check

    Logger.error('El usuario no existe: ' + username, OperationType.AUTH)
    return {
        'username': username,
        'ok': False
    }
