# from email.message import EmailMessage
# import ssl
# import smtplib
#
# sender = "pratikgopal.cha26@gmail.com"
# password = "svtitclscbvbxsai"
# receiver = "shingekititan024@gmail.com"
# subject = "This is a test email"
# body = """
# This is the first attempt to send email using new method from a video
# """
#
# email_sender = EmailMessage()
# email_sender['From'] = sender
# email_sender['To'] = receiver
# email_sender['Subject'] = subject
# email_sender.set_content(body)
#
#
# with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#     smtp.login(sender, password)
#     smtp.sendmail(sender, receiver, email_sender.as_string())
#
#
import bcrypt

# example password
password = 'password123'

# converting password to array of bytes
bytes = password.encode('utf-8')

# generating the salt
salt = bcrypt.gensalt(3)

# Hashing the password
hash = bcrypt.hashpw(bytes, salt)

print(hash)

password1 = 'password123'

# converting password to array of bytes
bytes1 = password.encode('utf-8')

# generating the salt
salt1 = bcrypt.gensalt(3)

# Hashing the password
hash1 = bcrypt.hashpw(bytes1, salt1)

if hash1 == hash:
    print(True)

