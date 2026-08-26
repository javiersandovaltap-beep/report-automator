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

logger = logging.getLogger(__name__)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def run_report():
    logger.info("Iniciando generación de reporte...")
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
        result = send_report(pdf)
        if result:
            logger.info(f"Reporte completado: {pdf}")
            return True
        else:
            logger.error("Falló el envío del reporte (ver los errores arriba)")
            return False
    except Exception:
        logger.exception("Error inesperado en la generación del reporte")
        return False


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
        run_report()
    elif args.schedule == "daily":
        schedule.every().day.at(SCHEDULE_TIME).do(run_report)
        logger.info(f"��⏰ Programado: todos los días a las {SCHEDULE_TIME}")
        while True:
            schedule.run_pending()
            time.sleep(60)
    elif args.schedule == "weekly":
        schedule.every().monday.at(SCHEDULE_TIME).do(run_report)
        logger.info(f"��⏰ Programado: todos los lunes a las {SCHEDULE_TIME}")
        while True:
            schedule.run_pending()
            time.sleep(60)
    elif args.schedule == "monthly":
        # Schedule for the first day of each month
        # schedule library doesn't have native monthly, so we do daily and check date
        def job():
            if datetime.now().astimezone().day == 1:
                run_report()
        schedule.every().day.at(SCHEDULE_TIME).do(job)
        logger.info(f"��������������⏰ Programado: primer día de cada mes a las {SCHEDULE_TIME}")
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        run_report()


if __name__ == "__main__":
    main()