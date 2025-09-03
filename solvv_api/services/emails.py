from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import BackgroundTasks
from pathlib import Path


from dotenv import load_dotenv
import os

load_dotenv() 

# Base directory where templates folder is located
BASE_DIR = Path(__file__).resolve().parent
from pathlib import Path

TEMPLATE_FOLDER = Path(__file__).resolve().parent.parent / "templates"


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),  # e.g., your Gmail or SMTP username
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),  # e.g., noreply@yourdomain.com
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=str(TEMPLATE_FOLDER)
)

async def send_thank_you_email(background_tasks: BackgroundTasks, recipient_email: str, name: str, course: str, link: str):
    """
    Sends a thank-you email with dynamic content.
    """
    message = MessageSchema(
        subject=f"Thank You for Joining {course}!",
        recipients=[recipient_email],
        template_body={
            "name": name,
            "course": course,
            "link": link
        },
        subtype="html"
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message, template_name="thank_you.html")
