#!/usr/bin/env python3
"""
page_creator/generate_charts.py

Reads  page_creator/initiatives.csv
Writes page_to_export/partials/chart_policy_area.html
       page_to_export/partials/chart_outcomes.html
       page_to_export/partials/chart_signatures_year.html
"""
import pandas as pd
import plotly.express as px
from pathlib import Path

CSV_PATH = Path(__file__).parent / "initiatives.csv"
OUT_DIR = Path(__file__).parent.parent / "page_to_export" / "partials"

COLORS = px.colors.qualitative.Plotly  # same palette as original nbconvert output

MARGIN = dict(l=20, r=20, t=50, b=20)
HEIGHT = 400
DIV_ARGS = dict(full_html=False, include_plotlyjs=False, config={"responsive": True})


def wrap_card(inner_html: str, extra_class: str = "") -> str:
    cls = f"card {extra_class}".strip()
    return f"""<div class="{cls}">
{inner_html}
</div>"""


def chart_policy_area(df: pd.DataFrame) -> str:
    agg = (
        df.groupby("primary_policy_area", as_index=False)["signatures_numeric"]
        .sum()
        .sort_values("signatures_numeric", ascending=False)
    )
    fig = px.bar(
        agg,
        x="primary_policy_area",
        y="signatures_numeric",
        color="primary_policy_area",
        color_discrete_sequence=COLORS,
        text_auto=".2s",
        title="Total Signatures by Policy Area",
        labels={
            "primary_policy_area": "Policy Area",
            "signatures_numeric": "Total Signatures",
        },
    )
    fig.update_layout(margin=MARGIN, height=HEIGHT, showlegend=True)
    return wrap_card(fig.to_html(**DIV_ARGS))


def chart_outcomes(df: pd.DataFrame) -> str:
    counts = df["outcome"].value_counts().reset_index()
    counts.columns = ["outcome", "count"]
    fig = px.pie(
        counts,
        names="outcome",
        values="count",
        hole=0.45,
        title="Initiatives by Commission Outcome",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_traces(textinfo="percent+label", textposition="inside")
    fig.update_layout(margin=MARGIN, height=HEIGHT, showlegend=False)
    return wrap_card(fig.to_html(**DIV_ARGS), extra_class="bottom-col")


def chart_signatures_year(df: pd.DataFrame) -> str:
    max_sig = df["signatures_numeric"].max()
    fig = px.scatter(
        df,
        x="registration_year",
        y="signatures_numeric",
        size="signatures_numeric",
        color="primary_policy_area",
        hover_name="title",
        color_discrete_sequence=COLORS,
        title="Signatures per Initiative by Year",
        labels={
            "registration_year": "Registration Year",
            "signatures_numeric": "Total Signatures",
            "primary_policy_area": "primary_policy_area",
        },
        size_max=60,
    )
    fig.update_layout(
        margin=MARGIN,
        height=HEIGHT,
        xaxis=dict(dtick=1),
        legend=dict(title_text="primary_policy_area", itemsizing="constant"),
    )
    return wrap_card(fig.to_html(**DIV_ARGS), extra_class="bottom-col")


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
