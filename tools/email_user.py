from typing import Dict
import smtplib
from email.message import EmailMessage
import os

def email_user(to_email: str, subject: str, body: str) -> dict:
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        raise EnvironmentError("Email credentials not set")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)

    return {
        "email_sent": True,
        "to": to_email
    }
