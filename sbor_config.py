import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


def create_service():
    CREDENTIALS_FILE = 'creds.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    return discovery.build('sheets', 'v4', http=httpAuth)
