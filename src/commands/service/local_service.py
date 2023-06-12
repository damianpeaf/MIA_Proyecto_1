from os import (
    path,
    mkdir,
    makedirs,
    rename,
    remove,
    walk,
    listdir
)
from shutil import rmtree, copy2, copytree
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

    def delete_resource(self, relative_path: str, file_name: str = None):

        if file_name:
            return self._delete_file(relative_path, file_name)
        else:
            return self._delete_directory(relative_path)

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

    def copy_resource(self, from_path: str, to_path: str):

        if path.isfile(path.join(LOCAL_ROOT_PATH, from_path)):
            return self._copy_file(from_path, to_path, path.basename(from_path))
        else:
            return self._copy_directory_content(from_path, to_path, False)

    def _copy_file(self, from_path: str, to_path: str, file_name: str):

        if from_path[0] == '/':
            from_path = from_path[1:]

        if to_path[0] == '/':
            to_path = to_path[1:]

        from_file_path = path.join(LOCAL_ROOT_PATH, from_path)

        print(from_file_path)

        if not path.exists(from_file_path):
            return {
                'ok': False,
                'msg': f"El archivo '{file_name}' no existe en la ruta '{from_path}'"
            }

        to_file_path = path.join(LOCAL_ROOT_PATH, to_path, file_name)

        if path.exists(to_file_path):
            return {
                'ok': False,
                'msg': f"El archivo '{file_name}' ya existe en la ruta '{to_path}'"
            }

        # Copy file
        copy2(from_file_path, to_file_path)

        return {
            'ok': True,
            'msg': f"Archivo '{file_name}' copiado con exito a la ruta '{to_path}'"
        }

    def _copy_directory_content(self, from_path: str, to_path: str, change_name: bool = False):

        if from_path[0] == '/':
            from_path = from_path[1:]

        if to_path[0] == '/':
            to_path = to_path[1:]

        from_dir_path = path.join(LOCAL_ROOT_PATH, from_path)
        if not path.exists(from_dir_path):
            return {
                'ok': False,
                'msg': f"El directorio '{from_path}' no existe"
            }

        to_dir_path = path.join(LOCAL_ROOT_PATH, to_path)

        if not path.exists(to_dir_path):
            makedirs(to_dir_path, exist_ok=True)

        # for storing warnings like: 'file already exists'
        warnings = []
        # TODO:

        for item in listdir(from_dir_path):
            item_path = path.join(from_dir_path, item)
            new_item_path = path.join(to_dir_path, item)

            if path.exists(new_item_path):
                if change_name:
                    new_item_path = self._get_unique_name(to_dir_path, item)
                    warnings.append(f"El archivo '{item}' ya existe en la carpeta destino. Se copiará como '{path.basename(new_item_path)}'")
                else:
                    warnings.append(f"No se copiará '{item}' porque ya existe en la carpeta destino.")
                    continue

            if path.isdir(item_path):
                # print(f'copy dir {item_path} to {new_item_path}')
                copytree(item_path, new_item_path)
            else:
                copy2(item_path, new_item_path)

        return {
            'ok': True,
            'msg': f"Contenido del directorio '{from_path}' copiado con exito a la ruta '{to_path}'",
            'warnings': warnings
        }

    def _get_unique_name(self, directory_path: str, name: str) -> str:

        base_name, ext = path.splitext(name)
        index = 1
        new_name = name
        while path.exists(path.join(directory_path, new_name)):
            new_name = f"{base_name} ({index}){ext}"
            index += 1
        return path.join(directory_path, new_name)
