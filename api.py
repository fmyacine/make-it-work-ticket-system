from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '../secret.json'
sheetID = '1AwbVTHtUjzMWOYFQ6kXLRgLxf4kBZ94IN4WmX7fKJOg'
cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)



def insert(name,familyname,phonenumber,email):
    try:
        service = build("sheets", "v4", credentials=cred)

        values = [
        [
            name,familyname,phonenumber,email
        ],
    ]


        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=sheetID,
                range='Sheet1!A2:K2',
                insertDataOption='INSERT_ROWS',
                valueInputOption='RAW',
                body=body
            ).execute()
        )
        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
