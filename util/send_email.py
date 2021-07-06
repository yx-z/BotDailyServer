import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Set


class Sender:
    def __init__(self, email: str, password: str, smtp_server: str, port: int):
        self.smtp_server = smtp_server
        self.port = port
        self.email_address = email
        self.password = password

    def send(self, recipients: Set[str], subject: str, html: str):
        logging.info(f"Sending from {self.email_address} to {recipients}")
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.email_address
        msg["To"] = ",".join(recipients)
        msg.attach(MIMEText(html, "html"))

        server = smtplib.SMTP_SSL(self.smtp_server, self.port)
        server.ehlo()
        server.login(self.email_address, self.password)
        server.sendmail(self.email_address, list(recipients), msg.as_string())
        server.close()
