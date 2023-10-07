import smtplib, ssl
from getpass import getpass
from email.message import EmailMessage
from email.utils import formataddr

from fastapi import FastAPI

class SMTPClient:

    def __init__(self, hostname: str, port: int, email: str, password: str):
        context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL(hostname, port, context=context)
        self.server.login(email, password)
    
    def send_message(self, subject: str, body: str, *, name: str, email: str,
                     to: str):
        msg = EmailMessage()
        msg['From'] = formataddr((name, email))
        msg['To'] = to
        msg['Subject'] = subject
        msg.set_content(body)
        self.server.send_message(msg)

app = FastAPI()
client = SMTPClient('mail.dhaownconstruction.com', 465,
                    'info@dhaownconstruction.com', getpass())
receiver = 'mukilteoacademy@gmail.com'
print('Logged in')

@app.post('/contact')
async def contact(comment: str, name: str, email: str):
    client.send_message('Contact', comment, name=name, email=email, to=receiver)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)