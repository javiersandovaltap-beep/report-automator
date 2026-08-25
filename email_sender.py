import logging
import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import EMAIL_PASSWORD, EMAIL_RECIPIENTS, EMAIL_SENDER, REPORT_TITLE

logger = logging.getLogger(__name__)


def send_report(pdf_path: str) -> bool:
    """Envía el reporte PDF por correo a todos los destinatarios configurados."""
    # Configuration pre-validation
    if not EMAIL_SENDER:
        logger.error("Error: EMAIL_SENDER is not set.")
        return False
    if not EMAIL_PASSWORD:
        logger.error("Error: EMAIL_PASSWORD is not set.")
        return False

    recipients = [r.strip() for r in EMAIL_RECIPIENTS if r.strip()]
    if not recipients:
        logger.error("Error: No valid email recipients configured.")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = ", ".join(recipients)
        msg["Subject"] = f"{REPORT_TITLE} — {datetime.now().astimezone().strftime('%d/%m/%Y')}"

        body = f"""
        <html><body>
        <h2 style="color:#1E3A5F">📊 {REPORT_TITLE}</h2>
        <p>Adjunto encontrarás el reporte automático generado el <b>{datetime.now().astimezone().strftime('%d/%m/%Y a las %H:%M')}</b>.</p>
        <p>Este reporte fue generado automáticamente. No responder a este correo.</p>
        <hr>
        <small style="color:#64748B">Report Automator · Sistema de Reportes Automáticos</small>
        </body></html>
        """
        msg.attach(MIMEText(body, "html"))

        with open(pdf_path, "rb") as f:
            attachment = MIMEApplication(f.read(), _subtype="pdf")
            attachment.add_header("Content-Disposition", "attachment", filename="reporte.pdf")
            msg.attach(attachment)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipients, msg.as_string())

        logger.info("Reporte enviado a: %s", ", ".join(recipients))
        return True
    except Exception:
        logger.exception("Error al enviar el reporte")
        return False