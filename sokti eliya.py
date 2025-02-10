from flask_mail import Message
from flask import render_template
from email import mail  # Flask-Mail instance
from qr import generate_ticket

def send_ticket_email(user_email, user_name, event_name, ticket_id):
    """Send a custom email with the ticket attached."""
    ticket_path = generate_ticket(user_name, event_name, ticket_id)

    # Render the email template
    email_html = render_template("email.html", 
                                 user_name=user_name, 
                                 event_name=event_name, 
                                 ticket_id=ticket_id, 
                                 ticket_link=f"http://yourwebsite.com/{ticket_path}")

    msg = Message(subject=f"Your Ticket for {event_name}",
                  sender="noreply@event.com",
                  recipients=[user_email])
    msg.html = email_html  # Set custom HTML template

    # Attach the ticket
    with open(ticket_path, "rb") as ticket_file:
        msg.attach(f"ticket_{ticket_id}.pdf", "application/pdf", ticket_file.read())

    mail.send(msg)
