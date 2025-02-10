from fpdf import FPDF
import qrcode
from io import BytesIO

def generate_ticket(user_name, event_name, ticket_id):
    """Generate a PDF ticket with a QR code."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Add Event Details
    pdf.cell(200, 10, f"Ticket for {event_name}", ln=True, align="C")
    pdf.cell(200, 10, f"Name: {user_name}", ln=True, align="C")
    pdf.cell(200, 10, f"Ticket ID: {ticket_id}", ln=True, align="C")

    # Generate QR Code
    qr_data = f"Ticket ID: {ticket_id} - Name: {user_name}"
    qr = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    
    # Save QR code as image and insert into PDF
    qr_filename = f"static/tickets/{ticket_id}.png"
    qr.save(qr_filename)
    pdf.image(qr_filename, x=80, y=50, w=50, h=50)

    # Save PDF
    pdf_filename = f"static/tickets/{ticket_id}.pdf"
    pdf.output(pdf_filename)
    
    return pdf_filename
