from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import os
load_dotenv()

def send_emails(email):
    sender = "pratikgopal.cha26@gmail.com"
    password = os.getenv("PASSWORD")
    receiver = email
    print(receiver)
    subject = "This is a test email"
    body = """
                    This is the first attempt to send email using new method from a video
                    """

    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        print("Testing this one")
        smtp.sendmail(sender, receiver, em.as_string())
        print("Sending email smtp")

    return True