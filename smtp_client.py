import smtplib, ssl
from email.message import EmailMessage
from getpass import getpass

email = 'info@dhaownconstruction.com'
password = getpass(f'Enter password for {email}: ')
receiver = 'mukilteoacademy@gmail.com'

# Create a secure SSL context
context = ssl.create_default_context()

server = smtplib.SMTP_SSL('mail.dhaownconstruction.com', 465, context=context)
# server = smtplib.SMTP('seattlepartners.us', 587)

server.login(email, password)

subject = input('Subject: ')
text = input('Body: ')
message = f'From: {email}\nTo: {receiver}\nSubject: {subject}\n\n{text}'

server.sendmail(email, receiver, message)

print('Email sent.')