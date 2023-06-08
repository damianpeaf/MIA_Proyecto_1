from os import path

from ..config import CommandEnvironment


def is_enviroment(value: str):

    if value is None:
        return False

    if value.lower() in ['local', 'cloud']:
        return True
    else:
        return False


def is_bool(value: str):

    if value is None:
        return False

    if value.lower() in ['true', 'false']:
        return True
    else:
        return False


def is_path(value: str):

    if path.isabs(path.normpath(value)):
        return True
    else:
        return False


def get_boolean(value: str):
    if value.lower() == 'true':
        return True
    else:
        return False


def get_enviroment(value: str):
    if value.lower() == 'local':
        return CommandEnvironment.LOCAL
    elif value.lower() == 'cloud':
        return CommandEnvironment.CLOUD
