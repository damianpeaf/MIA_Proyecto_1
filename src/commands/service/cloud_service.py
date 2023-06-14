from __future__ import print_function

from os import path
import tempfile
import io

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
from io import BytesIO

SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN_PATH = path.abspath(path.join(path.dirname(__file__), 'token.json'))

# ? Create an adapter for local/cloud services

ROOT_FOLDER_NAME = 'archivos'


class CloudFileService:

    proccesed_files = 0

    def reset_proccesed_files(self):
        CloudFileService.proccesed_files = 0

    def increment_proccesed_files(self, count: int = 1):
        CloudFileService.proccesed_files += count

    def get_proccesed_files(self):
        return CloudFileService.proccesed_files

    def __init__(self) -> None:
        self._drive_service = None
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        try:
            self._drive_service = build('drive', 'v3', credentials=creds, static_discovery=False)
        except HttpError as error:
            print(f'An error occurred with drive auth: {error}')

        self._root_id = self._get_root()

    def add_content(self, relative_path: str, body: str, is_add: bool = False) -> dict[str, str]:
        if self._drive_service is None:
            return

        # Check if is dir or file
        # If is dir, return error because is not supported, only files
        # If is file, add content to file

        file_name: str = relative_path.split('/')[-1]

        if file_name.find('.') == -1:
            return {
                'ok': False,
                'msg': 'No se puede agregar contenido a un directorio'
            }

        # Get file id
        resource_id = self._get_parent_id(relative_path)

        if resource_id is None:
            return {
                'ok': False,
                'msg': f'La ruta {relative_path} no existe'
            }

        # Check if file exists
        file_id = self._get_file_dir(resource_id, file_name)

        if file_id is None:
            return {
                'ok': False,
                'msg': f'No se encontró el archivo especificado en la ruta {relative_path}'
            }

        # Get file content
        file = self._drive_service.files().get(
            fileId=file_id, fields='id, name, mimeType').execute()

        if file.get('mimeType') != 'text/plain':
            return {
                'ok': False,
                'msg': 'No se puede agregar contenido a un archivo que no sea de texto plano'
            }

        # We can use this function to add/modify content
        new_content_file = body

        # If is add, we need to get the file content and add the new content
        if is_add:
            request = self._drive_service.files().get_media(fileId=file_id)
            file_content = request.execute().decode('utf-8')
            new_content_file = file_content + '\n' + body

        # Update/add file content
        media_body = MediaIoBaseUpload(
            io.BytesIO(new_content_file.encode('utf-8')), mimetype='text/plain')

        # Update file
        self._drive_service.files().update(
            fileId=file_id, media_body=media_body).execute()

        self.increment_proccesed_files()

        return {
            'ok': True,
            'msg': f'Se agregó el contenido al archivo {file_name}' if is_add else f'Se modificó el contenido del archivo {file_name}'
        }

    def create_file(self, name, content, path):

        try:
            if self._drive_service is None:
                return

            # Create directories
            parent_id = self._create_directories(path)

            # Search file exists aleready

            query = f"name='{name}' and '{parent_id}' in parents and trashed=false"

            response = self._drive_service.files().list(
                q=query, fields='files(id)').execute()
            files = response.get('files', [])

            if len(files) > 0:
                return {
                    'msg': f"El archivo '{name}' ya existe en la ruta especificada '{path}'",
                    'file_id': files[0].get('id'),
                    'ok': False
                }

            # Temp file

            with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                temp_path = temp_file.name

            with open(temp_path, 'w') as temp_file:
                temp_file.write(content)

            # Upload file

            file_metadata = {
                'name': name,
                'parents': [parent_id]
            }

            media = MediaFileUpload(temp_path, mimetype='text/plain')

            file = self._drive_service.files().create(
                body=file_metadata, media_body=media, fields='id').execute()

            self.increment_proccesed_files()

            return {
                'msg': f"Archivo '{name}' creado con exito en la ruta especificada '{path}'",
                'file_id': file.get('id'),
                'ok': True
            }

        except Exception as e:
            print(e)
            return {
                'msg': 'Ocurrio un error al crear el archivo',
                'file_id': None,
                'ok': False
            }

    def rename_file_dir(self, relative_path: str, new_name: str):

        if self._drive_service is None:
            return

        # Get parent id
        parent_id = self._get_parent_id(relative_path)

        # Check if parent exists
        if parent_id is None:
            return {
                'msg': 'No se encontró la ruta especificada',
                'ok': False
            }

        # Check if file exists
        file_to_rename_id = self._get_file_dir(
            parent_id, relative_path.split('/')[-1])

        if file_to_rename_id is None:
            return {
                'msg': 'No se encontró el archivo especificado',
                'ok': False
            }

        # Check if new name exists
        file_exists = self._get_file_dir(
            parent_id, new_name)

        if file_exists is not None and file_to_rename_id:
            return {
                'msg': 'Ya existe un archivo/directorio con ese nombre en la ruta especificada',
                'ok': False
            }

        # Rename
        file_metadata = {
            'name': new_name
        }

        try:
            file = self._drive_service.files().update(
                fileId=file_to_rename_id, body=file_metadata, fields='id').execute()

            self.increment_proccesed_files()

            return {
                'msg': 'Archivo renombrado con exito',
                'ok': True,
                'file_id': file.get('id')
            }
        except Exception as e:
            print(e)
            return {
                'msg': 'Ocurrio un error al renombrar el archivo',
                'ok': False
            }

    def delete_resource(self, relative_path: str, file_name: str = None):

        resource_id = self._search_resource(relative_path, file_name)

        resource_type = 'directorio' if file_name == None else 'archivo'

        if resource_id == None:
            return {
                'msg': f'No se encontró el {resource_type} especificado',
                'ok': False
            }

        try:

            self._drive_service.files().delete(fileId=resource_id).execute()

            self.increment_proccesed_files()

            return {
                'msg': f'{resource_type} eliminado con exito',
                'ok': True
            }
        except Exception as e:
            print(e)
            return {
                'msg': f'Ocurrio un error al {resource_type} el archivo',
                'ok': False
            }

    def _search_resource(self, relative_path: str, file_name: str = None) -> str:

        if self._drive_service is None:
            return

        full_path = relative_path

        if file_name:
            full_path += '/' + file_name

        parent_id = self._root_id

        for resource_name in full_path.split('/'):

            if resource_name == '':
                continue

            query = f"name='{resource_name}' and '{parent_id}' in parents and trashed=false"

            response = self._drive_service.files().list(
                q=query, fields='files(id)').execute()
            files = response.get('files', [])

            if len(files) > 0:
                parent_id = files[0].get('id')
            else:
                return None

        return parent_id

    def _create_folder(self, name, parent_id=None):

        if self._drive_service is None:
            return

        # ! no cuentan las carpetas eliminadas

        # check if folder exists
        query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"

        if parent_id:
            query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false"

        response = self._drive_service.files().list(
            q=query, fields='files(id)').execute()
        files = response.get('files', [])

        if len(files) > 0:
            return files[0].get('id')

        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        if parent_id:
            file_metadata['parents'] = [parent_id]

        file = self._drive_service.files().create(
            body=file_metadata, fields='id').execute()
        return file.get('id')

    def _get_root(self):

        if self._drive_service is None:
            return

        #  Create root folder
        return self._create_folder(ROOT_FOLDER_NAME)

    def _create_directories(self, path):
        # path looks like: /folder1/folder 2/folder3

        if self._drive_service is None:
            return

        parent_id = self._root_id

        for folder in path.split('/'):
            if folder == '':
                continue

            parent_id = self._create_folder(folder, parent_id)

        # last folder id
        return parent_id

    def _get_parent_id(self, path: str) -> str:

        if self._drive_service is None:
            return

        parent_id = self._root_id

        for folder_name in path.split('/')[:-1]:
            if folder_name == '':
                continue
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false"

            response = self._drive_service.files().list(
                q=query, fields='files(id)').execute()
            files = response.get('files', [])

            if len(files) > 0:
                parent_id = files[0].get('id')
            else:
                return None

        return parent_id

    def _get_file_dir(self, parent_id: str, name: str):

        if self._drive_service is None:
            return

        query = f"name='{name}' and '{parent_id}' in parents and trashed=false"

        response = self._drive_service.files().list(
            q=query, fields='files(id)').execute()
        files = response.get('files', [])

        if len(files) > 0:
            return files[0].get('id')
        else:
            return None

    # from path posibly include file name
    # change name is for decide if we want to change the name of the file if already exists or just add a warning
    def copy_resource(self, from_path: str, to_path: str, change_name: bool):

        from_id = self._search_resource(from_path)

        if from_id is None:
            return {
                'msg': 'No se encontró el recurso especificado de origen',
                'ok': False
            }

        to_id = self._search_resource(to_path)

        if to_id is None:
            return {
                'msg': 'No se encontró el recurso especificado de destino',
                'ok': False
            }

        # 'to' has to be a directory
        to_resource = self._drive_service.files().get(fileId=to_id, fields='id, name, mimeType').execute()

        if to_resource.get('mimeType') != 'application/vnd.google-apps.folder':
            return {
                'msg': 'El recurso de destino tiene que ser un directorio',
                'ok': False
            }

        # check if 'from' is a file or directory
        from_resource = self._drive_service.files().get(fileId=from_id, fields='id, name, mimeType').execute()

        # if 'from' is a directory, copy directory content (entire structure) into 'to' directory
        if from_resource.get('mimeType') == 'application/vnd.google-apps.folder':
            return self._copy_directory_content(from_resource, to_id, change_name)

        # just copy file into 'to' directory
        return self._copy_file(from_resource, to_id, change_name)

    def _copy_directory_content(self, from_resource: dict, to_id: str, change_name: bool):

        # Copy the from_resource content, not the directory itself

        # Get all files and directories inside from_resource
        query = f"'{from_resource.get('id')}' in parents and trashed=false"

        response = self._drive_service.files().list(
            q=query, fields='files(id, name, mimeType)').execute()
        files = response.get('files', [])

        warnings = []

        for file in files:

            # subdirectory
            if file.get('mimeType') == 'application/vnd.google-apps.folder':

                # check if directory exists in 'to' directory
                to_directory_id = self._get_file_dir(to_id, file.get('name'))

                # if not exists, create directory
                if to_directory_id is None:
                    # create directory with same content
                    created_folder = self._create_folder(file.get('name'), to_id)
                    self._copy_directory_content(file, created_folder, change_name)

                # if exists, evaluate change_name
                else:
                    if change_name:
                        # change name
                        new_name = self._get_new_name(file.get('name'), to_id)
                        created_folder = self._create_folder(new_name, to_id)
                        self._copy_directory_content(file, created_folder, change_name)
                        warnings.append(f"El directorio '{file.get('name')}' ya existe en la ruta de destino, se creó con el nombre '{new_name}'")
                    else:
                        warnings.append(f"El directorio '{file.get('name')}' ya existe en la ruta de destino")
                        continue

            # file
            else:

                # check if file exists in 'to' directory
                to_file_id = self._get_file_dir(to_id, file.get('name'))

                # if not exists, create file
                if to_file_id is None:
                    self._copy_file(file, to_id, change_name)

                # if exists, evaluate change_name
                else:
                    if change_name:
                        # change name
                        new_name = self._get_new_name(file.get('name'), to_id)
                        self._copy_file(file, to_id, change_name)
                        warnings.append(f"El archivo '{file.get('name')}' ya existe en la ruta de destino, se creó con el nombre '{new_name}'")
                    else:
                        warnings.append(f"El archivo '{file.get('name')}' ya existe en la ruta de destino")
                        continue

        return {
            'msg': 'Directorio copiado con exito',
            'ok': True,
            'warnings': warnings
        }

    def _copy_file(self, from_resource: dict, to_id: str, change_name: bool):

        # check if file exists in 'to' directory
        to_file_id = self._get_file_dir(to_id, from_resource.get('name'))

        # if not exists, create file
        if to_file_id is None:
            # copy file
            file_metadata = {
                'name': from_resource.get('name'),
                'parents': [to_id]
            }

            file = self._drive_service.files().copy(
                fileId=from_resource.get('id'), body=file_metadata).execute()

            self.increment_proccesed_files()

            return {
                'msg': f'Archivo {from_resource.get("name")} copiado con exito',
                'ok': True
            }

        # if exists, evaluate change_name
        else:
            if change_name:
                # change name
                new_name = self._get_new_name(from_resource.get('name'), to_id)
                file_metadata = {
                    'name': new_name,
                    'parents': [to_id]
                }

                file = self._drive_service.files().copy(
                    fileId=from_resource.get('id'), body=file_metadata).execute()

                self.increment_proccesed_files()

                return {
                    'msg': f'Archivo {from_resource.get("name")} copiado con exito con el nombre {new_name}',
                    'ok': True
                }

            else:
                return {
                    'msg': f'El archivo {from_resource.get("name")} ya existe en la ruta de destino',
                    'ok': False
                }

    # search for a new name for the file. Like file(1).txt or file(2).txt or file(3).txt ...
    def _get_new_name(self, name: str, parent_id: str) -> str:

        # check if file exists
        file_id = self._get_file_dir(parent_id, name)

        if file_id is None:
            return name

        # if exists, search for a new name
        counter = 1

        # Consider the extension
        file_name = name.split('.')[0]
        file_extension = ''

        if len(name.split('.')) > 1:
            file_extension = '.' + name.split('.')[1]

        while True:

            new_name = f'{file_name}({counter}){file_extension}'

            file_id = self._get_file_dir(parent_id, new_name)

            if file_id is None:
                return new_name

            counter += 1

    def transfer_resource(self, from_path: str, to_path: str):

        to_id = self._search_resource(to_path)

        if to_id is None:
            self._create_directories(to_path)

        # Copy resource
        resp = self.copy_resource(from_path, to_path, True)

        if not resp.get('ok'):
            return resp

        # Delete resource or directory content
        resource_id = self._search_resource(from_path)

        resource = self._drive_service.files().get(fileId=resource_id, fields='id, name, mimeType').execute()

        if resource.get('mimeType') == 'application/vnd.google-apps.folder':
            # Delete directory content, not the directory itself
            query = f"'{resource.get('id')}' in parents and trashed=false"

            response = self._drive_service.files().list(
                q=query, fields='files(id, name, mimeType)').execute()
            files = response.get('files', [])

            for file in files:
                self._drive_service.files().delete(fileId=file.get('id')).execute()
        else:
            # Delete file
            self._drive_service.files().delete(fileId=resource.get('id')).execute()

        return {
            'msg': 'Recurso transferido con exito',
            'ok': True,
            'warnings': resp.get('warnings') if resp.get('warnings') else []
        }

    def get_file_content(self, relative_path: str):

        if self._drive_service is None:
            return

        # Get file id
        resource_id = self._search_resource(relative_path)

        if resource_id is None:
            return {
                'ok': False,
                'msg': f'La ruta {relative_path} no existe'
            }

        # Check if file exists
        file = self._drive_service.files().get(
            fileId=resource_id, fields='id, name, mimeType').execute()

        if file.get('mimeType') != 'text/plain':
            return {
                'ok': False,
                'msg': 'No se puede obtener el contenido de un archivo que no sea de texto plano'
            }

        # Get file content
        request = self._drive_service.files().get_media(fileId=resource_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while done is False:
            status, done = downloader.next_chunk()

        return {
            'ok': True,
            'msg': fh.getvalue().decode('utf-8')
        }
