#!/usr/bin/env python3
import sys
from pathlib import Path

# Ensure project root (parent of page_creator/) is always on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from page_creator.partials.charts import (
    generate_chart_top_10_signatures,
    generate_chart_outcomes,
    generate_chart_signatures_cohorts,
)
from page_creator.partials.counters import generate_kpi_row
from page_creator.partials.lists import generate_currently_open

CSV_PATH = Path(__file__).parent / "data" / "initiatives.csv"
OUT_DIR = Path(__file__).parent.parent / "page_to_export" / "partials"


def main():
    df = pd.read_csv(CSV_PATH)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    charts = {
        "kpi_row.html": generate_kpi_row(df),
        "chart_top_10_signatures.html": generate_chart_top_10_signatures(df),
        "list_currently_open.html": generate_currently_open(df),
        "chart_outcomes.html": generate_chart_outcomes(df),
        "chart_signatures_cohorts.html": generate_chart_signatures_cohorts(df),
    }

    for filename, html in charts.items():
        path = OUT_DIR / filename
        path.write_text(html, encoding="utf-8")
        print(f"  wrote {path}  ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
