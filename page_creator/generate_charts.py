#!/usr/bin/env python3
import sys
from pathlib import Path

# Ensure project root (parent of page_creator/) is always on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from page_creator.partials.charts import (
    chart_policy_area,
    chart_outcomes,
    chart_signatures_year,
)

CSV_PATH = Path(__file__).parent / "initiatives.csv"
OUT_DIR = Path(__file__).parent.parent / "page_to_export" / "partials"


def main():
    df = pd.read_csv(CSV_PATH)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    charts = {
        "chart_policy_area.html": chart_policy_area(df),
        "chart_outcomes.html": chart_outcomes(df),
        "chart_signatures_year.html": chart_signatures_year(df),
    }

    for filename, html in charts.items():
        path = OUT_DIR / filename
        path.write_text(html, encoding="utf-8")
        print(f"  wrote {path}  ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
