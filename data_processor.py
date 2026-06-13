import pandas as pd
from config import DATA_FILE


def load_data(filepath: str = DATA_FILE) -> pd.DataFrame:
    """Carga datos desde CSV o Excel y los retorna como DataFrame."""
    if filepath.endswith(".xlsx"):
        return pd.read_excel(filepath)
    return pd.read_csv(filepath)


def generate_summary(df: pd.DataFrame) -> dict:
    """Genera métricas clave del dataset."""
    # Base contract – always present
    summary = {
        "total_rows": len(df),
        "columns": list(df.columns),
        "totals": {},            # will be replaced if numeric cols exist
        "averages": {},          # will be replaced if numeric cols exist
        "top_10": df.head(10),   # default fallback
    }

    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        return summary   # already contains the correct empty dicts and head(10)

    # Numeric columns present – override the three fields
    summary["totals"] = df[numeric_cols].sum().to_dict()
    summary["averages"] = df[numeric_cols].mean().round(2).to_dict()
    summary["top_10"] = df.sort_values(numeric_cols[0], ascending=False).head(10)
    return summary


def generate_chart(df: pd.DataFrame, output_path: str = "output/chart.png") -> str | None:
    """Genera un gráfico de barras y lo guarda como imagen."""
    import matplotlib.pyplot as plt
    import os

    os.makedirs("output", exist_ok=True)
    numeric_cols = df.select_dtypes(include="number").columns

    if len(df.columns) < 2 or len(numeric_cols) == 0:
        return None

    label_col = df.columns[0]
    value_col = numeric_cols[0]

    try:
        top = df.nlargest(10, value_col)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(top[label_col].astype(str), top[value_col], color="#2563EB")
        ax.set_title(f"Top 10 — {value_col}", fontsize=14, fontweight="bold")
        ax.set_xlabel(label_col)
        ax.set_ylabel(value_col)
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
    except Exception as e:
        print(f"⚠️  Advertencia: falló la generación del gráfico: {type(e).__name__}: {e}")
        return None

    return output_path