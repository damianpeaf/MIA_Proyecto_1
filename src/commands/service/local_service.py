from os import path, mkdir, makedirs
from .local_paths import LOCAL_ROOT_PATH


class LocalFileService:

    def __init__(self) -> None:
        self._create_root()

    def _create_root(self):
        if not path.exists(LOCAL_ROOT_PATH):
            mkdir(LOCAL_ROOT_PATH)

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
