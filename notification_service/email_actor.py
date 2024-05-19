import pykka
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from config import Config
from schemas import Templates, EmailActorMessage
from logging import info, error

config = Config()

class EmailSenderActor(pykka.ThreadingActor):
    def __init__(self):
        super().__init__()
        self.config = config.email

        try:
            self.server = smtplib.SMTP(self.config.server, self.config.port)
            self.server.starttls()
            self.server.login(self.config.address, self.config.password)
            info("SMTP server connection established.")
        except smtplib.SMTPException as e:
            error(f"Failed to connect to SMTP server: {e}")
            raise

        try:
            self.templates = Environment(loader=FileSystemLoader(config.templates_dir))
            info("Templates directory loaded successfully.")
        except Exception as e:
            error(f"Failed to load templates directory: {e}")
            raise

    def on_receive(self, message: EmailActorMessage):
        try:
            template = self.templates.get_template(message.template.value)
            subject, html_content = template.render(message.context).split("(__)")
            
            msg = MIMEMultipart()
            msg['From'] = self.config.address
            msg['To'] = message.recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(html_content, 'html'))

            self.server.send_message(msg)
            info(f"Email sent to {message.recipient}.")
        except Exception as e:
            error(f"Failed to send email to {message.recipient}: {e}")

    def on_stop(self):
        try:
            self.server.quit()
            info("SMTP server connection closed.")
        except Exception as e:
            error(f"Failed to close SMTP server connection: {e}")