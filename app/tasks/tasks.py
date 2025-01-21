from pydantic import EmailStr
from PIL import Image
from pathlib import Path
import smtplib

from app.tasks.celery_app import celery
from app.config import settings
from app.tasks.email_templates import create_booking_confirmation_template

@celery.task
def process_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized = im.resize((1000, 500))
    im_resized_icon = im.resize((200, 100))
    im_resized.save(f"app/static/images/resized_{im_path.name}")
    im_resized_icon.save(f"app/static/images/resized_icon_{im_path.name}")
    

@celery.task
def email_booking_confirm(
    booking: dict,
    email_to: EmailStr
):
    msg_content = create_booking_confirmation_template(booking, email_to)
    
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)