import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER     = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD   = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")
DATA_FILE        = os.getenv("DATA_FILE", "sample_data/sales_data.csv")
REPORT_TITLE     = os.getenv("REPORT_TITLE", "Reporte Automático")
COMPANY_NAME     = os.getenv("COMPANY_NAME", "Mi Empresa")
OUTPUT_PDF       = os.getenv("OUTPUT_PDF", "output/report.pdf")
SCHEDULE_TIME    = os.getenv("SCHEDULE_TIME", "08:00")
SCHEDULE_FREQUENCY = os.getenv("SCHEDULE_FREQUENCY", "daily")
CHART_OUTPUT_DIR   = os.getenv("CHART_OUTPUT_DIR", "output")
