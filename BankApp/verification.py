import smtplib
from email.mime.text import MIMEText

def send_verification_email(email: str, token: str):
    """Sends a verification email with the token"""
    verification_link = f"http://127.0.0.1:8000/verify/{token}"
    msg = MIMEText(f"Please click on the link to verify your email: {verification_link}")
    msg['Subject'] = 'Email Verification'
    msg['From'] = 'abhedayadhyani15041@gmail.com'
    msg['To'] = email

    # Example with Gmail (make sure to replace the login credentials)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login("abhedayadhyani15041@gmail.com", "7014224011")
    smtp_server.sendmail("abhedayadhyani15041@gmail.com", email, msg.as_string())
    smtp_server.quit()
    
