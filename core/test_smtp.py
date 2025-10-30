# test_smtp.py
import smtplib
from decouple import config

def test_smtp_connection():
    try:
        # Your SMTP settings
        smtp_server = "smtp.gmail.com"
        port = 587
        sender_email = config("EMAIL_ADDRESS")
        password = config("EMAIL_PASSWORD")
        
        print(f"Testing connection to {smtp_server}:{port}")
        print(f"Using email: {sender_email}")
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls()  # Enable security
        server.ehlo()  # Can be omitted
        
        # Login
        server.login(sender_email, password)
        print("✓ SMTP login successful!")
        
        server.quit()
        return True
        
    except Exception as e:
        print(f"✗ SMTP connection failed: {e}")
        return False

if __name__ == "__main__":
    test_smtp_connection()