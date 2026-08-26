import os
import re

from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER     = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD   = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENTS = [email.strip() for email in os.getenv("EMAIL_RECIPIENTS", "").split(",") if email.strip()]
DATA_FILE        = os.getenv("DATA_FILE", "sample_data/sales_data.csv")
REPORT_TITLE     = os.getenv("REPORT_TITLE", "Reporte Automático")
COMPANY_NAME     = os.getenv("COMPANY_NAME", "Mi Empresa")
OUTPUT_PDF       = os.getenv("OUTPUT_PDF", "output/report.pdf")
SCHEDULE_TIME    = os.getenv("SCHEDULE_TIME", "08:00")
SCHEDULE_FREQUENCY = os.getenv("SCHEDULE_FREQUENCY", "daily")
CHART_OUTPUT_DIR   = os.getenv("CHART_OUTPUT_DIR", "output")


def validate_config():
    """Validate configuration values.
    Currently validates SCHEDULE_TIME format (24-hour HH:MM).
    Raises ValueError with a clear message if invalid.
    """
    time_pattern = re.compile(r'^([01][0-9]|2[0-3]):([0-5][0-9])$')
    if not time_pattern.match(SCHEDULE_TIME):
        raise ValueError(f"Invalid SCHEDULE_TIME format: '{SCHEDULE_TIME}'. Expected HH:MM (24-hour).")
