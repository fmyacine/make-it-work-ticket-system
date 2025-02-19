from flask import Flask, request, jsonify, render_template,session,redirect
from flask_session import Session
from flask_mail import Mail, Message
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import format_cell_range, CellFormat, Color

from helper import login_required,validate_phone_number,is_valid_email

from api import insert,get_next_ticket_id,generate_event_ticket
app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.zoho.com'
app.config['MAIL_PORT'] = 587  # Use 587 if TLS
app.config['MAIL_USE_SSL'] = False  # Set to False if using TLS
app.config['MAIL_USE_TLS'] = True  # Set to True if using TLS
app.config['MAIL_USERNAME'] = 'no-reply@makeitwork.fwh.is'
app.config['MAIL_PASSWORD'] = 'yacineboy'  
app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@makeitwork.fwh.is'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST","GET"])
def login():
    
    if request.method == "POST":
        data = request.get_json()  # Get JSON data from request
        username = data.get("username")
        password = data.get("password")

        if username == "admin" and password == "cdecdawla":
            session["user_id"] = 1
            return jsonify({"success": True})  # Success response
        else:
            return jsonify({"success": False})  # Failure response
    if request.method == "GET":
        return render_template("login.html")

if not os.path.exists("static/tickets"):
    os.makedirs("static/tickets")

def send_ticket_email(user_email, user_name, ticket_id):
    """Send a custom email with the ticket attached."""
    ticket_path = generate_event_ticket(user_name, ticket_id)

    # Render custom email template
    email_html = render_template(
        "test.html", 
        user_name=user_name
    )

    msg = Message(subject=f"Your Ticket for Make It Work", recipients=[user_email])
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
    phone = data.get("number")



    if not user_name or not user_email:
        return jsonify({"error": "Name and Email are required!"}), 400

    if not validate_phone_number(phone) or not is_valid_email(user_email):
        return jsonify({"error": "Name and Email are required!"}), 400
    
    ticket_id = str(get_next_ticket_id())
    insert(user_name,phone,user_email,ticket_id)
    
    send_ticket_email(user_email, user_name, ticket_id)

    return jsonify({"message": "Ticket booked successfully!", "ticket_id": ticket_id})


@app.route("/admin",methods=["GET"])
@login_required

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
        
    id = data["id"].strip()
    
    sheet = get_google_sheet()
    # Find the row containing the person's name
    try:
        cell = sheet.find(id, in_column=1)  # Search in column A
        
        # Get the row number where the hash was found
        row_number = cell.row
        
        # Define the green fill format
        green_format = CellFormat(backgroundColor=Color(0.56, 0.93, 0.56))  # Light green (RGB 144, 238, 144)
        
        # Apply formatting to the entire row
        format_cell_range(sheet, f"A{row_number}:Z{row_number}", green_format)  # Adjust range as needed
        
        
        return jsonify({"message": "Check-in successful! Row highlighted."}), 200
    
    except gspread.exceptions.CellNotFound:
        return jsonify({"error": "ID not found!"}), 200
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
