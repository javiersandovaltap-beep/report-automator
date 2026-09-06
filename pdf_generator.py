import logging
import math
import os
import uuid
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from config import COMPANY_NAME, OUTPUT_PDF, REPORT_TITLE

logger = logging.getLogger(__name__)


def build_pdf(summary: dict, chart_path: str | None = None, output_path: str | None = None) -> str:
    """Genera un PDF profesional con métricas y tabla resumen."""
    if output_path is None:
        output_path = OUTPUT_PDF

    # Create directory for final output path
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Generate temporary file path with UUID to prevent race conditions
    # Insert .tmp<uuid> before the file extension
    root, ext = os.path.splitext(output_path)
    tmp_path = f"{root}.tmp{uuid.uuid4().hex[:8]}{ext}"

    doc = SimpleDocTemplate(
        tmp_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    story = []

    # --- Encabezado ---
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=20,
        textColor=colors.HexColor("#1E3A5F"),
        spaceAfter=6,
    )
    story.append(Paragraph(REPORT_TITLE, title_style))
    story.append(
        Paragraph(
            f"{COMPANY_NAME} · {datetime.now().astimezone().strftime('%d/%m/%Y %H:%M')}",
            styles["Normal"],
        )
    )
    story.append(
        HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563EB"))
    )
    story.append(Spacer(1, 0.5 * cm))

    # --- KPIs ---
    kpi_style = ParagraphStyle(
        "KPI",
        parent=styles["Normal"],
        fontSize=11,
        spaceAfter=4,
    )

    def _fmt(val):
        try:
            if math.isnan(val):
                return "N/A"
        except (TypeError, ValueError):
            pass
        return f"{val:,.2f}"

    story.append(Paragraph("Resumen General", styles["Heading2"]))
    story.append(
        Paragraph(f"Total de registros: {summary['total_rows']}", kpi_style)
    )
    for col, total in summary["totals"].items():
        story.append(Paragraph(f"Total {col}: {_fmt(total)}", kpi_style))
    for col, avg in summary["averages"].items():
        story.append(Paragraph(f"Promedio {col}: {_fmt(avg)}", kpi_style))
    story.append(Spacer(1, 0.5 * cm))

    # --- Gráfico ---
    if chart_path and os.path.exists(chart_path):
        try:
            story.append(Paragraph("Visualización", styles["Heading2"]))
            story.append(Image(chart_path, width=15 * cm, height=7 * cm))
            story.append(Spacer(1, 0.5 * cm))
        except Exception:
            logger.warning("No se pudo insertar el gráfico en el PDF", exc_info=True)

    # --- Tabla Top 10 ---
    story.append(Paragraph("Top 10 Registros", styles["Heading2"]))
    df_top = summary["top_10"]
    data = [list(df_top.columns)] + df_top.values.tolist()

    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A5F")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#EFF6FF")],
                ),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(table)

    try:
        doc.build(story)
        # Atomically move temp file to final location
        os.replace(tmp_path, output_path)
    except Exception:
        # Clean up temp file if it exists
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        raise

    return output_path
