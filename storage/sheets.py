import gspread
from oauth2client.service_account import ServiceAccountCredentials

import config
from storage.storage import Storage


class GoogleSheetsStorage(Storage):

    def __init__(self):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(config.GOOGLE_SECRET_PATH, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(config.GOOGLE_SHEET_FILE_NAME).sheet1

    def insert(self, values):
        self.sheet.append_row(values)

    def get_by_id(self, id):
        return []
