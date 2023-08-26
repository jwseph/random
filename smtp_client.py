import smtplib, ssl
from getpass import getpass
from email.message import EmailMessage
from email.utils import formataddr

email = 'info@dhaownconstruction.com'
password = getpass(f'Enter password for {email}: ')
receiver = 'mukilteoacademy@gmail.com'

context = ssl.create_default_context()
server = smtplib.SMTP_SSL('mail.dhaownconstruction.com', 465, context=context)

server.login(email, password)
print('Logged in as', email)

msg = EmailMessage()
msg['From'] = formataddr((input('Name to use: '), email))
msg['To'] = receiver
msg['Subject'] = input('Subject: ')
msg.set_content(input('Body: '))

server.send_message(msg)
print('Email sent.')