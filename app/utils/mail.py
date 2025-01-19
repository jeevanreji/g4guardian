# utils.py
from flask_mail import Message
from app import mail  # Import the mail instance configured in your main Flask app

def send_alert_email(user_email, subject, message_body):
    """
    Sends an alert email to the user.

    Args:
    user_email (str): Email address of the user
    subject (str): Subject of the email
    message_body (str): Body content of the email
    """
    msg = Message(subject, recipients=[user_email])
    msg.body = message_body
    
    try:
        mail.send(msg)
        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
