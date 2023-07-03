from email.message import EmailMessage
import ssl
import smtplib

sender = "pratikgopal.cha26@gmail.com"
password = "svtitclscbvbxsai"
receiver = "shingekititan024@gmail.com"
subject = "This is a test email"
body = """
This is the first attempt to send email using new method from a video
"""

email_sender = EmailMessage()
email_sender['From'] = sender
email_sender['To'] = receiver
email_sender['Subject'] = subject
email_sender.set_content(body)


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, email_sender.as_string())
