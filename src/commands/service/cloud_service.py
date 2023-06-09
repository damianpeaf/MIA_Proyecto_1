from __future__ import print_function

import os.path
import tempfile

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from io import BytesIO

SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN_PATH = os.path.join(os.path.dirname(__file__), 'token.json')

# ? Create an adapter for local/cloud services

ROOT_FOLDER_NAME = 'archivos'


class CloudFileService:

    def __init__(self) -> None:
        self._drive_service = None

        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        try:
            self._drive_service = build('drive', 'v3', credentials=creds)
        except HttpError as error:
            print(f'An error occurred with drive auth: {error}')

        self._root_id = self._get_root()

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

            print('Nombre de carpeta: ', folder_name, 'Parent id: ', parent_id)

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
                    'msg': 'El archivo ya existe en la ruta especificada',
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

            return {
                'msg': 'Archivo creado con exito',
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
