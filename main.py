import argparse
import logging
import os
import sys
import time
import uuid
from datetime import datetime

import schedule

from config import (
    CHART_OUTPUT_DIR,
    DATA_FILE,
    OUTPUT_PDF,
    SCHEDULE_TIME,
    check_full_config,
    validate_config,
)
from data_processor import generate_chart, generate_summary, load_data
from email_sender import send_report
from pdf_generator import build_pdf
from result import RunResult, log_run_outcome

logger = logging.getLogger(__name__)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def run_report(dry_run: bool = False):
    logger.info("Iniciando generación de reporte...")
    chart = None
    pdf = None
    try:
        # Generate unique run ID for this execution
        run_id = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]

        logger.info("Cargando datos...")
        df = load_data(DATA_FILE)
        logger.info("Datos cargados.")

        logger.info("Generando resumen...")
        summary = generate_summary(df)
        logger.info("Resumen generado.")

        logger.info("Generando gráfico...")
        # Generate unique chart path
        chart_path = os.path.join(CHART_OUTPUT_DIR, f"chart_{run_id}.png")
        chart = generate_chart(df, output_path=chart_path)
        if chart is None:
            logger.warning("Gráfico omitido: no se pudo generar o no aplica.")
        else:
            logger.info("Gráfico generado.")

        logger.info("Construyendo PDF...")
        # Generate unique PDF path
        pdf_dir = os.path.dirname(OUTPUT_PDF) if os.path.dirname(OUTPUT_PDF) else "output"
        pdf_path = os.path.join(pdf_dir, f"report_{run_id}.pdf")
        pdf = build_pdf(summary, chart, output_path=pdf_path)
        logger.info("PDF construido.")

        if dry_run:
            logger.info("Modo dry-run: omitiendo envío de correo")
            email_sent = False
            email_skipped = True
        else:
            logger.info("Enviando correo...")
            email_sent = send_report(pdf)
            email_skipped = False

        return RunResult(
            pdf_generated=True,
            pdf_path=pdf,
            chart_path=chart,
            email_sent=email_sent,
            email_skipped=email_skipped,
            error=None
        )
    except Exception as e:
        logger.exception("Error inesperado en la generación del reporte")
        return RunResult(
            pdf_generated=False,
            pdf_path=None,
            chart_path=chart,
            email_sent=False,
            email_skipped=False,
            error=str(e)
        )


def main():
    parser = argparse.ArgumentParser(description="Report Automator")
    parser.add_argument("--run-now",  action="store_true", help="Ejecutar inmediatamente")
    parser.add_argument("--schedule", choices=["daily", "weekly", "monthly"], help="Programar ejecución")
    parser.add_argument("--dry-run", "--no-email", action="store_true", dest="dry_run",
                     help="Ejecutar sin enviar correo (alias: --no-email)")
    parser.add_argument("--validate-config", action="store_true", help="Check .env configuration (schedule, data file, email) without running the pipeline")
    args = parser.parse_args()

    # Handle --validate-config flag
    if args.validate_config:
        try:
            check_full_config()
            logger.info("✅ Configuration is valid.")
            sys.exit(0)
        except ValueError as e:
            logger.error(str(e))
            sys.exit(1)

    # Validate configuration
    try:
        validate_config()
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    if args.run_now:
        result = run_report(dry_run=args.dry_run)
        log_run_outcome(result, logger)
        sys.exit(0 if (result.email_sent or result.email_skipped) else (2 if result.pdf_generated else 1))
    elif args.schedule == "daily":
        def job():
            result = run_report(dry_run=args.dry_run)
            log_run_outcome(result, logger)
        schedule.every().day.at(SCHEDULE_TIME).do(job)
        logger.info(f"��⏰ Programado: todos los días a las {SCHEDULE_TIME}")
        while True:
            schedule.run_pending()
            time.sleep(60)
    elif args.schedule == "weekly":
        def job():
            result = run_report(dry_run=args.dry_run)
            log_run_outcome(result, logger)
        schedule.every().monday.at(SCHEDULE_TIME).do(job)
        logger.info(f"��⏰ Programado: todos los lunes a las {SCHEDULE_TIME}")
        while True:
            schedule.run_pending()
            time.sleep(60)
    elif args.schedule == "monthly":
        # Schedule for the first day of each month
        # schedule library doesn't have native monthly, so we do daily and check date
        def job():
            if datetime.now().astimezone().day == 1:
                result = run_report(dry_run=args.dry_run)
                log_run_outcome(result, logger)
        schedule.every().day.at(SCHEDULE_TIME).do(job)
        logger.info(f"��������������⏰ Programado: primer día de cada mes a las {SCHEDULE_TIME}")
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        result = run_report(dry_run=args.dry_run)
        log_run_outcome(result, logger)
        sys.exit(0 if (result.email_sent or result.email_skipped) else (2 if result.pdf_generated else 1))


if __name__ == "__main__":
    main()