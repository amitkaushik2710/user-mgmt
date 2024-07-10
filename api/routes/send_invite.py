from fastapi import FastAPI, UploadFile, File, Form, APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from core.config import settings

app = FastAPI()

class EmailSchema(BaseModel):
    email_to: str
    subject: str

router = APIRouter()

templates = Jinja2Templates(directory="templates")
env = Environment(loader=FileSystemLoader('templates'))

@router.post("/")
async def send_invite(
    email_to: str = Form(...),
    subject: str = Form(...),
    cc: Optional[str] = Form(None),
    bcc: Optional[str] = Form(None),
    attachments: List[UploadFile] = File(...),
):
    try:
        send_email(email_to, subject, attachments, cc, bcc)
        return JSONResponse(content={"message": "Email sent successfully"})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to send email: {str(e)}"}, status_code=500)

def send_email(email_to: str, subject: str, attachments: Optional[List[UploadFile]], cc : str | None, bcc : str | None):
    sender_email = settings.EMAIL_USER
    sender_password = settings.EMAIL_PASSWORD

    template = env.get_template('send_invite.html')
    html_content = template.render(subject=subject)
    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email_to
    msg["Subject"] = subject
    
    if cc:
        if isinstance(cc, str):
            cc = [cc] 
        msg["Cc"] = ", ".join(cc)

    if bcc:
        if isinstance(bcc, str):
            bcc = [bcc] 
        msg["Bcc"] = ", ".join(bcc)

    msg.attach(MIMEText(html_content, 'html'))

    if attachments:
        for attachment in attachments:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment.filename}",
            )
            msg.attach(part)

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:  
        server.starttls()  
        server.login(sender_email, sender_password) 
        text = msg.as_string()
        server.sendmail(sender_email, email_to, text)
