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
LOCK_FILE_PATH   = os.path.abspath(os.getenv("LOCK_FILE_PATH", "report_automator.lock"))


def check_schedule_time():
    """Validate SCHEDULE_TIME format (24-hour HH:MM).
    Raises ValueError with a clear message if invalid.
    Used by validate_config() and check_full_config().
    """
    time_pattern = re.compile(r'^([01][0-9]|2[0-3]):([0-5][0-9])$')
    if not time_pattern.match(SCHEDULE_TIME):
        raise ValueError(f"Invalid SCHEDULE_TIME format: '{SCHEDULE_TIME}'. Expected HH:MM (24-hour).")


def validate_config():
    """Validate configuration values.
    Currently validates SCHEDULE_TIME format (24-hour HH:MM).
    Raises ValueError with a clear message if invalid.
    This is the pre-flight check that runs on every invocation.
    """
    check_schedule_time()


def check_data_file_exists():
    """Check if DATA_FILE exists.
    Raises ValueError if the file does not exist.
    Used exclusively by check_full_config().
    """
    if not os.path.isfile(DATA_FILE):
        raise ValueError(f"DATA_FILE not found: '{DATA_FILE}'.")


def check_email_config():
    """Check if EMAIL_SENDER, EMAIL_PASSWORD, and EMAIL_RECIPIENTS are configured.
    Raises ValueError listing any missing variables.
    Used exclusively by check_full_config().
    """
    missing = []
    if not EMAIL_SENDER:
        missing.append("EMAIL_SENDER")
    if not EMAIL_PASSWORD:
        missing.append("EMAIL_PASSWORD")
    if not EMAIL_RECIPIENTS:  # Empty list is falsy
        missing.append("EMAIL_RECIPIENTS")

    if missing:
        raise ValueError(f"Missing required email configuration: {', '.join(missing)}.")


def check_full_config():
    """Run all configuration checks and aggregate errors.
    Used exclusively by --validate-config CLI command.
    Does not affect the pre-flight validate_config() check.
    """
    errors = []

    try:
        check_schedule_time()
    except ValueError as e:
        errors.append(str(e))

    try:
        check_data_file_exists()
    except ValueError as e:
        errors.append(str(e))

    try:
        check_email_config()
    except ValueError as e:
        errors.append(str(e))

    if errors:
        raise ValueError("\n".join(errors))
