import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config
import redis
import requests



EMAIL = config("EMAIL")
APP_PASSWORD  = config("APP_PASSWORD")




def send_email(receiver, otp):
    sender_email = EMAIL
    receiver_email = receiver
    password = APP_PASSWORD 
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Bituz tasdiqlash kodi"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f""
    html = f"<html><body><p>Sizning Bituz platformasidagi emailingizni tasdiqlash kodingiz - {otp}.\nHech kimga bermang!!! </p></body></html>"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    return False
