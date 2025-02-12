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


from fpdf import FPDF
import qrcode
def generate_qr_code(ticket_id, user_name):
    """Generate a QR code and return its file path."""
    qr_data = f"Ticket ID: {ticket_id}\nName: {user_name}"
    qr = qrcode.make(qr_data)
    qr_path = f"static/tickets/{ticket_id}.png"
    qr.save(qr_path)
    return qr_path

def generate_event_ticket(user_name, event_name, ticket_id):
    """Generate a PDF ticket with event details and a QR code."""
    
    # Initialize PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Event Name
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, event_name, ln=True, align="L")
    pdf.ln(10)

    # Event Details
    pdf.set_font("Arial", "B", 20)
    pdf.multi_cell(0, 10, "Salon de l'Emploi Emploitic Connect 2024")
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Accès au Salon Emploitic Connect", ln=True)
    
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, "La Coupole, Complexe Olympique Mohamed Boudiaf, Dely Ibrahim 16000, Algérie" )
    
    pdf.cell(0, 10, "Samedi 27 janvier 2024 à 09:00 - Dimanche 28 janvier 2024 à 15:00 (heure : Algérie)", ln=True)
    
    # Order Info
    pdf.cell(0, 10, "Commande #8784135539", ln=True)
    pdf.cell(0, 10, "Commande gratuite", ln=True)

    # Order Details
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Informations de commande", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"Commande nº 8784135539. Commandé par {user_name} le 2024-01-26T15:21:19.491000" )

    # Generate and add QR code
    qr_code_path = generate_qr_code(ticket_id, user_name)
    
    try:
        pdf.image(qr_code_path, x=150, y=120, w=40)
    except Exception as e:
        print(f"Error adding QR code: {e}")

    # Ticket ID below QR code
    pdf.set_xy(150, 165)
    pdf.set_font("Arial", "", 8)
    pdf.cell(40, 10, f"{ticket_id}", ln=True, align="C")

    # Save the PDF
    pdf_path = f"static/tickets/{ticket_id}.pdf"
    pdf.output(pdf_path)

    return pdf_path