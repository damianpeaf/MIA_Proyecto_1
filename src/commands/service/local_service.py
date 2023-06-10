from os import (
    path,
    mkdir,
    makedirs,
    rename,
    remove
)
from shutil import rmtree
from .local_paths import LOCAL_ROOT_PATH


class LocalFileService:

    def __init__(self) -> None:
        self._create_root()

    def _create_root(self):
        if not path.exists(LOCAL_ROOT_PATH):
            mkdir(LOCAL_ROOT_PATH)

    def add_content(self, relative_path: str, body: str) -> dict[str, str]:
        relative_path = relative_path[1:] if relative_path[0] == '/' else relative_path

        # Create path LOCAL_ROOT_PATH + relative_path
        dir_path = path.join(LOCAL_ROOT_PATH, relative_path)

        # Check if dir exists
        if not path.exists(dir_path):
            return {
                'ok': False,
                'msg': f"La ruta '{relative_path}' no existe"
            }

        # Check if dir is a file
        if path.isdir(dir_path):
            return {
                'ok': False,
                'msg': f"La ruta '{relative_path}' es un directorio"
            }

        # Add content to file
        with open(dir_path, 'a') as file:
            file.write(body)

        return {
            'ok': True,
            'msg': f"Contenido agregado con exito a '{relative_path}'"
        }

    def create_file(self, name: str, body: str, relative_path: str):

        # relative path starts with '/'
        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        # Create path LOCAL_ROOT_PATH + relative_path
        dir_path = path.join(LOCAL_ROOT_PATH, relative_path)
        # crate folders (even if they exist or not)
        makedirs(dir_path, exist_ok=True)

        file_path = path.join(dir_path, name)

        # if file exists return
        if path.exists(file_path):
            return {
                'ok': False,
                'msg': f"El archivo '{name}' ya existe en la ruta '{relative_path}'"
            }

        # create file
        with open(file_path, 'w') as file:
            file.write(body)

        return {
            'ok': True,
            'msg': f"Archivo '{name}' creado con exito en la ruta '{relative_path}'"
        }

    def delete_resource(self, relative_path: str, file_name: str = None):

        if file_name:
            return self._delete_file(relative_path, file_name)
        else:
            return self._delete_directory(relative_path)

    def modify_resource(self, relative_path: str, body: str) -> dict:

        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        dir_path = path.join(LOCAL_ROOT_PATH, relative_path)

        if not path.exists(dir_path):
            return {
                'ok': False,
                'msg': f"La ruta '{relative_path}' no existe"
            }

        if path.isdir(dir_path):
            return {
                'ok': False,
                'msg': f"La ruta '{relative_path}' es un directorio"
            }

        with open(dir_path, 'w') as file:
            file.write(body)

        return {
            'ok': True,
            'msg': f"Contenido modificado con exito en '{relative_path}'"
        }

    def rename_file_dir(self, relative_path: str, new_name: str):

        # Validate if dir/file exists
        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        dir_path = path.join(LOCAL_ROOT_PATH, relative_path)
        base_name = path.dirname(dir_path)
        new_path = path.join(base_name, new_name)

        if path.exists(new_path):
            return {
                'ok': False,
                'msg': f"El archivo '{new_name}' ya existe en la ruta '{relative_path}'"
            }

        # Rename
        rename(dir_path, new_path)

        return {
            'ok': True,
            'msg': f"Archivo '{relative_path}' renombrado con exito"
        }

    def _delete_file(self, relative_path: str, file_name: str):

        # Validate if dir/file exists
        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        file_path = path.join(LOCAL_ROOT_PATH, relative_path, file_name)

        if not path.exists(file_path):
            return {
                'ok': False,
                'msg': f"El archivo '{file_name}' no existe en la ruta '{relative_path}'"
            }

        # Delete
        remove(file_path)

        return {
            'ok': True,
            'msg': f"Archivo '{relative_path}' eliminado con exito"
        }

    def _delete_directory(self, relative_path: str):

        # Validate if dir/file exists
        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        dir_path = path.join(LOCAL_ROOT_PATH, relative_path)

        if not path.exists(dir_path):
            return {
                'ok': False,
                'msg': f"El directorio '{relative_path}' no existe"
            }

        # Delete directory even if it has files
        rmtree(dir_path)

        return {
            'ok': True,
            'msg': f"Directorio '{relative_path}' eliminado con exito"
        }
