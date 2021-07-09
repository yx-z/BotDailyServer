import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Set, Union


class Sender:
    def __init__(self, email: str, password: str, smtp_server: str, port: int):
        self.smtp_server = smtp_server
        self.port = port
        self.email_address = email
        self.password = password

    def send(self, recipient_emails: Union[str, Set[str]], subject: str, body: str):
        logging.info(f"Sending email from {self.email_address} to {recipient_emails}")
        logging.info(f"Subject: {subject}\nBody: {body}")
        if isinstance(recipient_emails, str):
            recipient_emails = {recipient_emails}
        logging.info(f"Sending from {self.email_address} to {recipient_emails}")
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.email_address
        msg["To"] = ",".join(recipient_emails)
        msg.attach(MIMEText(body, "html"))

        server = smtplib.SMTP_SSL(self.smtp_server, self.port)
        server.ehlo()
        server.login(self.email_address, self.password)
        server.sendmail(self.email_address, list(recipient_emails), msg.as_string())
        server.close()
