from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
sheetID = '1tUdJce9qB0fp1IUDyOEF_NNyJz_6Bm7_G2U28ql6cps'
google_credentials = os.getenv("GOOGLE_CLOUD_CREDENTIALS")
cred = service_account.Credentials.from_service_account_file(google_credentials, scopes=SCOPES)

import re

def insert(fullname, phonenumber, email, tkt):
    hashed_string = generate_ticket_hash(fullname, str(tkt))

    try:
        service = build("sheets", "v4", credentials=cred)

        # Data to insert
        values = [[hashed_string.strip(), fullname, phonenumber, email]]
        body = {"values": values}

        # Insert the row
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=sheetID,
                range='Sheet1!A:D',  # Append to columns A to D
                insertDataOption='INSERT_ROWS',
                valueInputOption='RAW',
                body=body
            ).execute()
        )

        # Extract the row number from the updated range
        updated_range = result.get('updates', {}).get('updatedRange', '')  # e.g., "Sheet1!A35:D35"
        print(updated_range)
        match = re.search(r'!A(\d+):D\d+', updated_range)

        print(match)
        if match:
            row_number = int(match.group(1))  # Convert extracted number to integer
        else:
            print("Could not determine the row number.")
            return

        # Set background color for the newly inserted row
        requests = [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": 0,  # Default sheet ID (change if necessary)
                        "startRowIndex": row_number - 1,  # Convert to zero-based index
                        "endRowIndex": row_number,
                        "startColumnIndex": 0,
                        "endColumnIndex": 26,  # Columns A to D
                    },
                    "cell": {"userEnteredFormat": {"backgroundColor": {"red": 1, "green": 1, "blue": 1}}},  # White color
                    "fields": "userEnteredFormat.backgroundColor",
                }
            }
        ]

        # Send the formatting request
        body = {
            "requests": requests
        }

        response = service.spreadsheets().batchUpdate(
            spreadsheetId=sheetID,
            body=body
        ).execute()

        print("Response:", response)
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
import hashlib

def generate_ticket_hash(user_name, ticket_id):
    raw_data = f"{user_name}{ticket_id}".encode()  # Combine user + ticket ID
    md5_hash = hashlib.md5(raw_data).hexdigest()  # Generate MD5 hash
    return md5_hash


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


from fpdf import FPDF
import qrcode
def generate_qr_code(ticket_id, user_name):
    """Generate a QR code with properly formatted JSON data."""
    qr_data = {
        "name": user_name,
        "tickt": ticket_id,
        "id": generate_ticket_hash(user_name , ticket_id)
    }

    # Convert to JSON string before encoding
    qr_data_json = json.dumps(qr_data)

    qr = qrcode.make(qr_data_json)  # Encode as JSON string, not a Python dictionary
    qr_path = f"static/tickets/{ticket_id}.png"
    qr.save(qr_path)
    return qr_path


def generate_event_ticket(user_name,  ticket_id):
    """Generate a PDF ticket with event details and a QR code."""
    
    # Initialize PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    page_width = pdf.w

    # Image properties
    # Get page width
    page_width = pdf.w

    # Image properties
    image_path = "static/CDECLOGO.png"  # Make sure the path is correct
    image_width = 50  
    image_x = (page_width - image_width) / 3  
    image_y = 10  

    pdf.image(image_path, x=image_x, y=image_y, w=image_width)

    image_path = "static/makeitworklogojpg.jpg"  # Make sure the path is correct
    image_width = 50  # Adjust based on your image size
    image_x = 2 * (page_width - image_width) / 3  # Center it
    image_y = 10  # Adjust Y position to place it at the top

    # Add image
    pdf.image(image_path, x=image_x, y=image_y, w=image_width)

    # Move cursor below the image
    pdf.ln(60)  # Adjust spacing based on image height

    # Event Details
    pdf.set_font("Arial", "B", 20)
    pdf.multi_cell(0, 10, "Make It Work 2025")
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Ticket for Make It Work Event", ln=True)
    
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, "Saad Dahleb Blida University, Auditorim, Ouled Yaich 09000, Algeria" )
    
    pdf.cell(0, 10, "Tuesday 25 Febraury 2025 at 09:00 - samedi 25 february 2025 At 15:00 (heure : Algérie)", ln=True)
    
    # Order Details
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Informations de commande", ln=True)
    pdf.set_font("Arial", "", 12)
    from datetime import datetime

    pdf.multi_cell(0, 10, f"Commandé par {user_name} le {datetime.now().isoformat()}")
    pdf.ln(40)
    # Generate and add QR code
    qr_code_path = generate_qr_code(ticket_id, user_name)
    
    try:
        pdf.ln(40)
        pdf.image(qr_code_path, x=150, y=120, w=40)
        pdf.ln(40)  
    except Exception as e:
        print(f"Error adding QR code: {e}")

    # Ticket ID below QR code
    pdf.set_xy(150, 165)
    pdf.set_font("Arial", "", 8)
    pdf.cell(40, 10, f"{ticket_id}", ln=True, align="C")

    pdf_path = f"static/tickets/{ticket_id}.pdf"
    pdf.output(pdf_path)

    return pdf_path
