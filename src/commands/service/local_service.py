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

    proccessed_files = 0

    def reset_proccesed_files(self):
        LocalFileService.proccessed_files = 0

    def increment_proccesed_files(self, count: int = 1):
        LocalFileService.proccessed_files += count

    def get_proccesed_files(self):
        return LocalFileService.proccessed_files

    def __init__(self) -> None:
        self._create_root()

    def _create_root(self):
        if not path.exists(LOCAL_ROOT_PATH):
            mkdir(LOCAL_ROOT_PATH)

    def create_directory(self, name: str, relative_path: str, change_name: bool = True):
        # relative path starts with '/'
        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        # Create path LOCAL_ROOT_PATH + relative_path
        dir_path = path.join(LOCAL_ROOT_PATH, relative_path, name)

        warnings = []

        if path.exists(dir_path):
            if change_name:
                dir_path = self._get_unique_name(path.join(LOCAL_ROOT_PATH, relative_path), name)
                warnings.append(f"El directorio '{name}' ya existe en la ruta '{relative_path}'. Se creará como '{path.basename(dir_path)}'")
            else:
                return {
                    'ok': False,
                    'msg': f"El directorio '{name}' ya existe en la ruta '{relative_path}'"
                }

        # Create directory
        makedirs(dir_path, exist_ok=True)

        return {
            'ok': True,
            'msg': f"Directorio '{name}' creado con exito en la ruta '{relative_path}'",
            'name': path.basename(dir_path),
            'warnings': warnings
        }

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

        self.increment_proccesed_files()

        return {
            'ok': True,
            'msg': f"Contenido agregado con exito a '{relative_path}'"
        }

    def create_file(self, name: str, body: str, relative_path: str, change_name: bool = False):

        # relative path starts with '/'
        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        # Create path LOCAL_ROOT_PATH + relative_path
        dir_path = path.join(LOCAL_ROOT_PATH, relative_path)
        # crate folders (even if they exist or not)
        makedirs(dir_path, exist_ok=True)

        file_path = path.join(dir_path, name)

        warnings = []

        # if file exists return
        if path.exists(file_path):

            if change_name:
                file_path = self._get_unique_name(dir_path, name)
                warnings.append(f"El archivo '{name}' ya existe en la ruta '{relative_path}'. Se creará como '{path.basename(file_path)}'")
            else:
                return {
                    'ok': False,
                    'msg': f"El archivo '{name}' ya existe en la ruta '{relative_path}'"
                }

        # create file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(body)

        self.increment_proccesed_files()

        return {
            'ok': True,
            'msg': f"Archivo '{name}' creado con exito en la ruta '{relative_path}'",
            'name': path.basename(file_path),
            'warnings': warnings
        }

    def delete_resource(self, relative_path: str, file_name: str = None, count_as_processed: bool = True):

        if file_name:
            return self._delete_file(relative_path, file_name, count_as_processed)
        else:
            return self._delete_directory(relative_path, count_as_processed)

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

        with open(dir_path, 'w', encoding='utf-8') as file:
            file.write(body)

        self.increment_proccesed_files()

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

        if not path.exists(dir_path):
            return {
                'ok': False,
                'msg': f"El archivo '{relative_path}' no existe"
            }

        if path.exists(new_path):
            return {
                'ok': False,
                'msg': f"El archivo '{new_name}' ya existe en la ruta '{relative_path}'"
            }

        # Rename
        rename(dir_path, new_path)

        self.increment_proccesed_files()

        return {
            'ok': True,
            'msg': f"Archivo '{relative_path}' renombrado con exito"
        }

    def _delete_file(self, relative_path: str, file_name: str, count_as_processed: bool = False):

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

        if count_as_processed:
            self.increment_proccesed_files()

        return {
            'ok': True,
            'msg': f"Archivo '{relative_path}' eliminado con exito"
        }

    def _delete_directory(self, relative_path: str, count_as_processed: bool = False):

        # Validate if dir/file exists
        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        dir_path = path.join(LOCAL_ROOT_PATH, relative_path)

        if not path.exists(dir_path):
            return {
                'ok': False,
                'msg': f"El directorio '{relative_path}' no existe"
            }

        # is a directory
        if not path.isdir(dir_path):
            return {
                'ok': False,
                'msg': f"La ruta '{relative_path}' no es un directorio"
            }

        # get file count (including subdirectories)
        if count_as_processed:
            file_count = 0
            for _, _, files in walk(dir_path):
                file_count += len(files)

            self.increment_proccesed_files(file_count)

        # Delete directory even if it has files
        rmtree(dir_path)

        return {
            'ok': True,
            'msg': f"Directorio '{relative_path}' eliminado con exito"
        }

    def _delete_directory_content(self, relative_path: str):

        # Validate if dir/file exists
        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        dir_path = path.join(LOCAL_ROOT_PATH, relative_path)

        if not path.exists(dir_path):
            return {
                'ok': False,
                'msg': f"El directorio '{relative_path}' no existe"
            }

        # Delete directory content
        for item in listdir(dir_path):
            item_path = path.join(dir_path, item)
            if path.isdir(item_path):
                rmtree(item_path)
            else:
                remove(item_path)

        return {
            'ok': True,
            'msg': f"Contenido del directorio '{relative_path}' eliminado con exito"
        }

    def copy_resource(self, from_path: str, to_path: str, change_name: bool = False):

        if from_path[0] == '/':
            from_path = from_path[1:]

        if path.isfile(path.join(LOCAL_ROOT_PATH, from_path)):
            return self._copy_file(from_path, to_path, path.basename(from_path), change_name)
        else:
            return self._copy_directory_content(from_path, to_path, change_name)

    def _copy_file(self, from_path: str, to_path: str, file_name: str, change_name: bool = False):

        if from_path[0] == '/':
            from_path = from_path[1:]

        if to_path[0] == '/':
            to_path = to_path[1:]

        from_file_path = path.join(LOCAL_ROOT_PATH, from_path)

        if not path.exists(from_file_path):
            return {
                'ok': False,
                'msg': f"El archivo '{file_name}' no existe en la ruta '{from_path}'"
            }

        if not path.exists(path.join(LOCAL_ROOT_PATH, to_path)):
            return {
                'ok': False,
                'msg': f"El directorio destino '{to_path}' no existe"
            }

        if not path.isdir(path.join(LOCAL_ROOT_PATH, to_path)):
            return {
                'ok': False,
                'msg': f"La ruta destino '{to_path}' no es un directorio"
            }

        to_file_path = path.join(LOCAL_ROOT_PATH, to_path, file_name)

        if path.exists(to_file_path):
            if change_name:
                to_file_path = self._get_unique_name(path.join(LOCAL_ROOT_PATH, to_path), file_name)
            else:
                return {
                    'ok': False,
                    'msg': f"El archivo '{file_name}' ya existe en la ruta '{to_path}'"
                }

        # Copy file
        copy2(from_file_path, to_file_path)

        self.increment_proccesed_files()

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
                'msg': f"El directorio origen '{from_path}' no existe"
            }

        to_dir_path = path.join(LOCAL_ROOT_PATH, to_path)

        if not path.exists(to_dir_path):
            # makedirs(to_dir_path, exist_ok=True)
            return {
                'ok': False,
                'msg': f"El directorio destino '{to_path}' no existe"
            }

        if not path.isdir(to_dir_path):
            return {
                'ok': False,
                'msg': f"La ruta destino '{to_path}' no es un directorio"
            }

        # for storing warnings like: 'file already exists'
        warnings = []

        for item in listdir(from_dir_path):
            item_path = path.join(from_dir_path, item)
            new_item_path = path.join(to_dir_path, item)

            if path.exists(new_item_path):
                if change_name:
                    new_item_path = self._get_unique_name(to_dir_path, item)
                    item_type = 'directorio' if path.isdir(item_path) else 'archivo'
                    warnings.append(f"El {item_type} '{item}' ya existe en la carpeta destino. Se copiará como '{path.basename(new_item_path)}'")
                else:
                    warnings.append(f"No se copiará '{item}' porque ya existe en la carpeta destino.")
                    continue

            if path.isdir(item_path):

                file_count = 0
                for _, _, files in walk(item_path):
                    file_count += len(files)

                self.increment_proccesed_files(file_count)

                copytree(item_path, new_item_path)
            else:
                self.increment_proccesed_files()
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
            new_name = f"{base_name}({index}){ext}"
            index += 1
        return path.join(directory_path, new_name)

    def transfer_resource(self, from_path: str, to_path: str):

        if from_path[0] == '/':
            from_path = from_path[1:]

        if to_path[0] == '/':
            to_path = to_path[1:]

        to_relative_path = to_path[1:] if to_path[0] == '/' else to_path

        # create directory if not exists
        if not path.exists(path.join(LOCAL_ROOT_PATH, to_relative_path)):
            makedirs(path.join(LOCAL_ROOT_PATH, to_relative_path), exist_ok=True)

        resp = self.copy_resource(from_path, to_path, True)

        if not resp['ok']:
            return resp

        if path.isfile(path.join(LOCAL_ROOT_PATH, from_path)):
            # remove filename from from_path
            self.delete_resource(path.dirname(from_path), path.basename(from_path), False)
        else:
            self._delete_directory_content(from_path)

        return {
            'ok': True,
            'msg': f"'{from_path}' transferido con exito a la ruta '{to_path}'",
            'warnings': resp['warnings'] if 'warnings' in resp else []
        }

    def get_file_content(self, relative_path: str) -> dict:

        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        file_path = path.join(LOCAL_ROOT_PATH, relative_path)

        if not path.exists(file_path):
            return {
                'ok': False,
                'msg': f"El archivo '{relative_path}' no existe"
            }

        if path.isdir(file_path):
            return {
                'ok': False,
                'msg': f"La ruta '{relative_path}' es un directorio"
            }

        with open(file_path, 'r', encoding='utf-8') as file:
            return {
                'ok': True,
                'msg': f"Contenido del archivo '{relative_path}' obtenido con exito",
                'body': file.read()
            }

    def cloud_backup(self, cloud_service):
        # saves all files and directories in cloud

        warnings = []

        for item in listdir(LOCAL_ROOT_PATH):
            item_path = path.join(LOCAL_ROOT_PATH, item)

            if path.isdir(item_path):
                resp = cloud_service.create_directory(item, '/')

                if resp.get('ok'):
                    warnings += resp.get('warnings')

                self._cloud_backup_directory(item_path, cloud_service, item, warnings)

            else:
                content = ''

                with open(item_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                resp = cloud_service.create_file(item, content, '/', True)
                if resp.get('ok'):
                    warnings += resp.get('warnings')

        return {
            'ok': True,
            'msg': f"Todos los archivos y directorios fueron guardados en la nube",
            'warnings': warnings
        }

    def _cloud_backup_directory(self, local_directory_path: str, cloud_service, relative_path: str, warnings: list):

        for item in listdir(local_directory_path):
            item_path = path.join(local_directory_path, item)

            if path.isdir(item_path):
                resp = cloud_service.create_directory(item, relative_path)
                if resp.get('ok'):
                    warnings += resp.get('warnings')
                self._cloud_backup_directory(item_path, cloud_service, relative_path + '/' + item, warnings)

            else:
                content = ''

                with open(item_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                resp = cloud_service.create_file(item, content, relative_path, True)
                if resp.get('ok'):
                    warnings += resp.get('warnings')
