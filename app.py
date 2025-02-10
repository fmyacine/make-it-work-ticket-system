from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from fpdf import FPDF
import qrcode
from io import BytesIO
import random
import os

from api import insert
app = Flask(__name__)

# 🔹 Flask-Mail Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "fed.myacine@gmail.com"
app.config["MAIL_PASSWORD"] = "ewos dkvc henc rylu"
app.config["MAIL_DEFAULT_SENDER"] = "fed.myacine@gmail.com"

mail = Mail(app)

# 🔹 Ensure 'static/tickets' folder exists
if not os.path.exists("static/tickets"):
    os.makedirs("static/tickets")

# ====================================
# 1️⃣ Generate QR Code
# ====================================
def generate_qr_code(ticket_id, user_name):
    """Generate a QR code for the ticket."""
    qr_data = f"{user_name}"
    qr = qrcode.make(qr_data)
    qr_path = f"static/tickets/{ticket_id}.png"
    qr.save(qr_path)
    return qr_path

# ====================================
# 2️⃣ Generate PDF Ticket
# ====================================
def generate_ticket(user_name, event_name, ticket_id):
    """Generate a PDF ticket with a QR code."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    pdf.cell(200, 10, f"Ticket for {event_name}", ln=True, align="C")
    pdf.cell(200, 10, f"Name: {user_name}", ln=True, align="C")
    pdf.cell(200, 10, f"Ticket ID: {ticket_id}", ln=True, align="C")

    # Add QR code
    qr_path = generate_qr_code(ticket_id, user_name)
    pdf.image(qr_path, x=80, y=50, w=50, h=50)

    # Save PDF
    pdf_path = f"static/tickets/{ticket_id}.pdf"
    pdf.output(pdf_path)

    return pdf_path

# ====================================
# 3️⃣ Send Ticket Email
# ====================================
def send_ticket_email(user_email, user_name, event_name, ticket_id):
    """Send a custom email with the ticket attached."""
    ticket_path = generate_ticket(user_name, event_name, ticket_id)

    # Render custom email template
    email_html = render_template(
        "email.html", 
        user_name=user_name, 
        event_name=event_name, 
        ticket_id=ticket_id, 
        ticket_link=f"http://yourwebsite.com/{ticket_path}"
    )

    msg = Message(subject=f"Your Ticket for {event_name}", recipients=[user_email])
    msg.html = email_html

    # Attach the ticket PDF
    with open(ticket_path, "rb") as ticket_file:
        msg.attach(f"ticket_{ticket_id}.pdf", "application/pdf", ticket_file.read())

    mail.send(msg)

# ====================================
# 4️⃣ API Route to Book Ticket
# ====================================
@app.route("/book-ticket", methods=["POST"])
def book_ticket():
    """Receive JSON request, generate ticket, and send via email."""
    data = request.get_json()

    user_name = data.get("name")
    user_email = data.get("email")
    event_name = data.get("event_name", "Tech Conference 2025")  
    ticket_id = f"TKT-{random.randint(1000,9999)}"
    insert(user_name,1,user_email)
    if not user_name or not user_email:
        return jsonify({"error": "Name and Email are required!"}), 400

    send_ticket_email(user_email, user_name, event_name, ticket_id)

    return jsonify({"message": "Ticket booked successfully!", "ticket_id": ticket_id})


@app.route("/admin",methods=["GET"])
def admin():
    return render_template("admin.html")

import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Connect to Google Sheets
def get_google_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name("your_google_credentials.json", ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)
    sheet = client.open("Your Google Sheet Name").sheet1  # Select first sheet
    return sheet

@app.route("/check_in", methods=["POST"])
def check_in():
    data = request.json
    name = data.get("name")
    
    sheet = get_google_sheet()
    
    # Find the row containing the person's name
    cell = sheet.find(name)
    if cell:
        return jsonify({"message": "Check-in successful!"}), 200
    return jsonify({"error": "Name not found!"}), 404


# ====================================
# Run Flask App
# ====================================
if __name__ == "__main__":
    app.run(debug=True)
