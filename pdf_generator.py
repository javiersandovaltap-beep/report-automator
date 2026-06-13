import os
import math
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from config import REPORT_TITLE, COMPANY_NAME, OUTPUT_PDF


def build_pdf(summary: dict, chart_path: str = None) -> str:
    """Genera un PDF profesional con métricas y tabla resumen."""
    os.makedirs("output", exist_ok=True)

    doc = SimpleDocTemplate(
        OUTPUT_PDF,
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
            f"{COMPANY_NAME} · {datetime.now().strftime('%d/%m/%Y %H:%M')}",
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
            pass

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

    doc.build(story)
    return OUTPUT_PDF