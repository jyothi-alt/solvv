# solvv_api/core/mail.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel

class MailSettings(BaseModel):
    MAIL_USERNAME: str = "your_smtp_username"
    MAIL_PASSWORD: str = "your_smtp_password"
    MAIL_FROM: str = "no-reply@evolvv.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.yourprovider.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

mail_conf = ConnectionConfig(
    MAIL_USERNAME=MailSettings().MAIL_USERNAME,
    MAIL_PASSWORD=MailSettings().MAIL_PASSWORD,
    MAIL_FROM=MailSettings().MAIL_FROM,
    MAIL_PORT=MailSettings().MAIL_PORT,
    MAIL_SERVER=MailSettings().MAIL_SERVER,
    MAIL_STARTTLS=MailSettings().MAIL_TLS,
    MAIL_SSL_TLS=MailSettings().MAIL_SSL,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER="solvv_api/templates"  # create this folder
)

fast_mail = FastMail(mail_conf)
