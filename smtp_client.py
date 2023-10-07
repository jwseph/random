import smtplib, ssl
from getpass import getpass
from email.message import EmailMessage
from email.utils import formataddr

email = 'info@dhaownconstruction.com'
password = getpass(f'Enter password for {email}: ')
# receiver = 'mukilteoacademy@gmail.com'
# email = 'admin@advangers.com'
receiver = 'mukilteoacademy@gmail.com'

context = ssl.create_default_context()
print('Context created, trying to connect')
server = smtplib.SMTP_SSL('mail.advangers.com', 465, context=context)
print('Logging in...')
server.login(email, password)
print('Logged in as', email)

msg = EmailMessage()
msg['From'] = formataddr((input('Name to use: '), email))
msg['To'] = receiver
msg['Subject'] = input('Subject: ')
msg.set_content(input('Body: '))

server.send_message(msg)
print('Email sent.')