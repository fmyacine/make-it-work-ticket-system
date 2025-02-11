from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = './secret.json'
sheetID = '1tUdJce9qB0fp1IUDyOEF_NNyJz_6Bm7_G2U28ql6cps'
cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)



def insert(fullname,phonenumber,email):
    try:
        service = build("sheets", "v4", credentials=cred)

        values = [
        [
            fullname,phonenumber,email
        ],
    ]


        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=sheetID,
                range='Sheet1!A2:D2',
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

TICKET_FILE = "last_ticket_id.txt"
import os
def get_next_ticket_id():
    
    if not os.path.exists(TICKET_FILE):
        last_ticket_id = -1  # Start from 0 when first ticket is created
    else:
        with open(TICKET_FILE, "r") as file:
            last_ticket_id = int(file.read().strip())

    # Increment ticket ID
    next_ticket_id = (last_ticket_id + 1) % 10000  # Loop back after 9999

    # Save the new ticket ID
    with open(TICKET_FILE, "w") as file:
        file.write(str(next_ticket_id))

    return f"TKT-{next_ticket_id:04d}"
