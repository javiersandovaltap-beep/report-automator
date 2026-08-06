import argparse
import schedule
import time
import logging
from data_processor import load_data, generate_summary, generate_chart
from pdf_generator import build_pdf
from email_sender import send_report
from config import DATA_FILE, SCHEDULE_TIME

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def run_report():
    logging.info("Iniciando generación de reporte...")
    try:
        logging.info("Cargando datos...")
        df = load_data(DATA_FILE)
        logging.info("Datos cargados.")

        logging.info("Generando resumen...")
        summary = generate_summary(df)
        logging.info("Resumen generado.")

        logging.info("Generando gráfico...")
        chart = generate_chart(df)
        if chart is None:
            logging.warning("Gráfico omitido: no se pudo generar o no aplica.")
        else:
            logging.info("Gráfico generado.")

        logging.info("Construyendo PDF...")
        pdf = build_pdf(summary, chart)
        logging.info("PDF construido.")

        logging.info("Enviando correo...")
        result = send_report(pdf)
        if result:
            logging.info(f"Reporte completado: {pdf}")
            return True
        else:
            logging.error("Falló el envío del reporte (ver los errores arriba)")
            return False
    except Exception as e:
        logging.error(f"Error inesperado en la generación del reporte: {type(e).__name__}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Report Automator")
    parser.add_argument("--run-now",  action="store_true", help="Ejecutar inmediatamente")
    parser.add_argument("--schedule", choices=["daily", "weekly"], help="Programar ejecución")
    args = parser.parse_args()

    if args.run_now:
        run_report()
    elif args.schedule == "daily":
        schedule.every().day.at(SCHEDULE_TIME).do(run_report)
        logging.info(f"��⏰ Programado: todos los días a las {SCHEDULE_TIME}")
        while True:
            schedule.run_pending()
            time.sleep(60)
    elif args.schedule == "weekly":
        schedule.every().monday.at(SCHEDULE_TIME).do(run_report)
        logging.info(f"��⏰ Programado: todos los lunes a las {SCHEDULE_TIME}")
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        run_report()


if __name__ == "__main__":
    main()