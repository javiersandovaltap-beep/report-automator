import argparse
import logging
import sys
import time
from datetime import datetime

import schedule

from config import DATA_FILE, SCHEDULE_TIME, validate_config
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


def run_report():
    logger.info("Iniciando generación de reporte...")
    chart = None
    try:
        logger.info("Cargando datos...")
        df = load_data(DATA_FILE)
        logger.info("Datos cargados.")

        logger.info("Generando resumen...")
        summary = generate_summary(df)
        logger.info("Resumen generado.")

        logger.info("Generando gráfico...")
        chart = generate_chart(df)
        if chart is None:
            logger.warning("Gráfico omitido: no se pudo generar o no aplica.")
        else:
            logger.info("Gráfico generado.")

        logger.info("Construyendo PDF...")
        pdf = build_pdf(summary, chart)
        logger.info("PDF construido.")

        logger.info("Enviando correo...")
        email_sent = send_report(pdf)
        return RunResult(
            pdf_generated=True,
            pdf_path=pdf,
            chart_path=chart,
            email_sent=email_sent,
            error=None
        )
    except Exception as e:
        logger.exception("Error inesperado en la generación del reporte")
        return RunResult(
            pdf_generated=False,
            pdf_path=None,
            chart_path=chart,
            email_sent=False,
            error=str(e)
        )


def main():
    parser = argparse.ArgumentParser(description="Report Automator")
    parser.add_argument("--run-now",  action="store_true", help="Ejecutar inmediatamente")
    parser.add_argument("--schedule", choices=["daily", "weekly", "monthly"], help="Programar ejecución")
    args = parser.parse_args()

    # Validate configuration
    try:
        validate_config()
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    if args.run_now:
        result = run_report()
        log_run_outcome(result, logger)
        sys.exit(0 if result.email_sent else (2 if result.pdf_generated else 1))
    elif args.schedule == "daily":
        def job():
            result = run_report()
            log_run_outcome(result, logger)
        schedule.every().day.at(SCHEDULE_TIME).do(job)
        logger.info(f"��⏰ Programado: todos los días a las {SCHEDULE_TIME}")
        while True:
            schedule.run_pending()
            time.sleep(60)
    elif args.schedule == "weekly":
        def job():
            result = run_report()
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
                result = run_report()
                log_run_outcome(result, logger)
        schedule.every().day.at(SCHEDULE_TIME).do(job)
        logger.info(f"��������������⏰ Programado: primer día de cada mes a las {SCHEDULE_TIME}")
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        result = run_report()
        log_run_outcome(result, logger)
        sys.exit(0 if result.email_sent else (2 if result.pdf_generated else 1))


if __name__ == "__main__":
    main()