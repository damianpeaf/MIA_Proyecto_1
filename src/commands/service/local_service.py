from os import (
    path,
    mkdir,
    makedirs,
    rename
)
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

        # create file
        file_path = path.join(dir_path, name)
        with open(file_path, 'w') as file:
            file.write(body)

    def rename_file_dir(self, relative_path: str, new_name: str):

        # Validate if dir/file exists
        if relative_path[0] == '/':
            relative_path = relative_path[1:]

        dir_path = path.join(LOCAL_ROOT_PATH, relative_path)
        base_name = path.dirname(dir_path)
        new_path = path.join(base_name, new_name)

        if path.exists(new_path):
            return False

        # Rename
        rename(dir_path, new_path)

        return True
