from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from fpdf import FPDF
import qrcode
from io import BytesIO
import random
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import format_cell_range, CellFormat, Color


from api import insert,get_next_ticket_id,generate_event_ticket
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

def send_ticket_email(user_email, user_name, event_name, ticket_id):
    """Send a custom email with the ticket attached."""
    ticket_path = generate_event_ticket(user_name, ticket_id)

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
        msg.attach(f"{ticket_id}.pdf", "application/pdf", ticket_file.read())

    mail.send(msg)

@app.route("/book-ticket", methods=["POST"])
def book_ticket():
    """Receive JSON request, generate ticket, and send via email."""
    data = request.get_json()

    user_name = data.get("name")
    user_email = data.get("email")
    event_name = data.get("Make It Work")
    ticket_id = str(get_next_ticket_id())
    insert(user_name,1,user_email,ticket_id)

    if not user_name or not user_email:
        return jsonify({"error": "Name and Email are required!"}), 400

    send_ticket_email(user_email, user_name, event_name, ticket_id)

    return jsonify({"message": "Ticket booked successfully!", "ticket_id": ticket_id})


@app.route("/admin",methods=["GET"])
def admin():
    return render_template("admin.html")


def get_google_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name("./secret.json", ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)
    sheet = client.open("make it work").sheet1
    return sheet
import json
@app.route("/check_in", methods=["POST"])
def check_in():
    print("scanned")
    data = request.json
    data = data["name"]

    if isinstance(data, str):
        try:
            data = json.loads(data)  # Convert back to dictionary
        except json.JSONDecodeError:
            return {"error": "Invalid QR code data format"}, 400
        
    sheet = get_google_sheet()
    id = data["id"]
    print(id)
    # Find the row containing the person's name
    cell = sheet.find(id)
    if cell:
        # Color the row green if name is found
        row_number = cell.row
        range_to_color = f"A{row_number}:Z{row_number}"  
        fmt = CellFormat(backgroundColor=Color(0, 1, 0))  
        format_cell_range(sheet, range_to_color, fmt)
        print({"message": "Check-in successful!"})
        
        return jsonify({"message": "Check-in successful!"}), 200
    return jsonify({"error": "Name not found!"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
