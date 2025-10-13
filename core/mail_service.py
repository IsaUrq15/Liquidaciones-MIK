from fastapi_mail import FastMail, MessageSchema
from core.mail_config import conf
from pathlib import Path
from typing import Optional

async def enviar_correo(destinatario: str, asunto: str, body: str, pdf_path: Optional[str] = None):
    attachments = []

    if pdf_path and Path(pdf_path).is_file():
        attachments.append(str(Path(pdf_path).resolve()))  # <-- solo la ruta

    message = MessageSchema(
        subject=asunto,
        recipients=[destinatario],
        body=body,
        subtype="html",
        attachments=attachments  # lista de rutas de archivos
    )

    fm = FastMail(conf)
    await fm.send_message(message)