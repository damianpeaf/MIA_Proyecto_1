from __future__ import print_function

import os.path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN_PATH = os.path.join(os.path.dirname(__file__), 'token.json')

# ? Create an adapter for local/cloud services


class CloudFileService:

    def __init__(self) -> None:
        self._drive_service = None

        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        try:
            self._drive_service = build('drive', 'v3', credentials=creds)
        except HttpError as error:
            print(f'An error occurred with drive auth: {error}')

    def _create_root(self):
        pass
