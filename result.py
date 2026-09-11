from dataclasses import dataclass


@dataclass
class RunResult:
    pdf_generated: bool
    pdf_path: str | None
    chart_path: str | None
    email_sent: bool
    email_skipped: bool = False
    lock_skipped: bool = False
    error: str | None = None


def log_run_outcome(result: RunResult, logger) -> None:
    """Logs the final outcome of a report run based on its RunResult.
    Must be called exactly once per run_report() invocation, at every call site."""
    if not result.pdf_generated:
        logger.error("No se pudo generar el reporte: %s", result.error)
    elif result.email_skipped:
        logger.info("Reporte completado (dry-run, envío de correo omitido): %s", result.pdf_path)
    elif result.email_sent:
        logger.info("Reporte completado: %s", result.pdf_path)
    else:
        logger.error("Falló el envío del reporte (ver los errores arriba)")