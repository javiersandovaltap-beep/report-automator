import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENTS, REPORT_TITLE


def send_report(pdf_path: str) -> bool:
    """Envía el reporte PDF por correo a todos los destinatarios configurados."""
    # Configuration pre-validation
    if not EMAIL_SENDER:
        print("Error: EMAIL_SENDER is not set.")
        return False
    if not EMAIL_PASSWORD:
        print("Error: EMAIL_PASSWORD is not set.")
        return False
    # Normalize recipients: strip whitespace and discard empty entries
    recipients = [r.strip() for r in EMAIL_RECIPIENTS if r.strip()]
    if not recipients:
        print("Error: No valid email recipients configured.")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = ", ".join(recipients)
        msg["Subject"] = f"{REPORT_TITLE} — {datetime.now().strftime('%d/%m/%Y')}"

        body = f"""
        <html><body>
        <h2 style="color:#1E3A5F">📊 {REPORT_TITLE}</h2>
        <p>Adjunto encontrarás el reporte automático generado el <b>{datetime.now().strftime('%d/%m/%Y a las %H:%M')}</b>.</p>
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

        print(f" Reporte enviado a: {', '.join(recipients)}")
        return True
    except Exception as e:
        print(f" Error sending report: {type(e).__name__}: {e}")
        return False