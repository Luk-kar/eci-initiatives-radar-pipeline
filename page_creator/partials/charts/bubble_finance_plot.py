import numpy as np
import pandas as pd
import plotly.graph_objects as go

from page_creator.config import DIV_ARGS, HEIGHT, MARGIN
from page_creator.utils import wrap_card

# ── Bubble category colour scheme ─────────────────────────────────────────────
BUBBLE_COLORS: dict[str, str] = {
    "Law Active/Passed": "#2E7D32",
    "Commission Engaged": "#FFA726",
    "Rejected": "#C62828",
    "Waiting for Response": "#9E9E9E",
    "Unsuccessful Collection": "#DEDEDE",
}

_CATEGORY_ORDER = list(BUBBLE_COLORS.keys())

# ── current_status → bubble category ─────────────────────────────────────────
_STATUS_TO_CATEGORY: dict[str, str] = {
    "Law Passed": "Law Active/Passed",
    "Law Active": "Law Active/Passed",
    "Commission Engaged": "Commission Engaged",
    "Law Promised": "Commission Engaged",
    "Action Plan Created": "Commission Engaged",
    "Being Studied": "Commission Engaged",
    "Rejected Legislation": "Rejected",
    "Rejected": "Rejected",
    "Waiting for Response": "Waiting for Response",
    "Collection Ongoing": "Waiting for Response",
    "Collection Unsuccessful": "Unsuccessful Collection",
    "Withdrawn": "Unsuccessful Collection",
}


def _map_status(status: str) -> str | None:
    if pd.isna(status):
        return None
    s = str(status).strip()
    # Exact-match lookup first
    if s in _STATUS_TO_CATEGORY:
        return _STATUS_TO_CATEGORY[s]
    # Fallback substring checks
    if "Law Active" in s or "Law Passed" in s:
        return "Law Active/Passed"
    if any(k in s for k in ("Law Promised", "Action Plan", "Being Studied", "Commission Engaged")):
        return "Commission Engaged"
    if "Rejected" in s:
        return "Rejected"
    if any(k in s for k in ("Unsuccessful", "Withdrawn")):
        return "Unsuccessful Collection"
    return "Waiting for Response"


def _parse_funding(value) -> float:
    """Parse comma-formatted funding strings (e.g. '12,980.15') to float."""
    if pd.isna(value) or value == "" or value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return 0.0


# ── Main chart generator ──────────────────────────────────────────────────────

def generate_chart_bubble_plot(df: pd.DataFrame) -> str:
    df = df.copy()

    df["funding_numeric"] = df["funding_total"].apply(_parse_funding)
    df["bubble_category"] = df["current_status"].apply(_map_status)
    df = df[df["bubble_category"].notna()].reset_index(drop=True)

    # For log scale, replace €0 with a small display offset
    _LOG_ZERO_DISPLAY = 200
    df["funding_display"] = df["funding_numeric"].apply(
        lambda v: _LOG_ZERO_DISPLAY if v == 0.0 else v
    )
    df["has_zero_funding"] = df["funding_numeric"] == 0.0

    # Build y-axis positions with jitter for visual separation
    present = [c for c in _CATEGORY_ORDER if c in df["bubble_category"].values]
    cat_index = {c: i for i, c in enumerate(present)}
    df["y_pos"] = df["bubble_category"].map(cat_index)

    rng = np.random.default_rng(42)
    df["y_jitter"] = df["y_pos"] + rng.uniform(-0.15, 0.15, len(df))

    # Marker sizes: log-normalised to [8, 43]
    log_f = np.log10(df["funding_display"])
    span = log_f.max() - log_f.min()
    df["marker_size"] = (
        (log_f - log_f.min()) / span * 35 + 8 if span > 0 else 20
    )
    df["marker_size"] = df["marker_size"].fillna(15).clip(lower=5, upper=50)

    fig = go.Figure()

    for category in present:
        cat_df = df[df["bubble_category"] == category]

        hover_texts = []
        for _, row in cat_df.iterrows():
            funding_label = (
                "€0 (No funding data)"
                if row["has_zero_funding"]
                else f"€{row['funding_numeric']:,.0f}"
            )
            hover_texts.append(
                f"<b>{str(row['title'])[:65]}</b><br>"
                f"Funding: {funding_label}<br>"
                f"Status: {row['current_status']}"
            )

        fig.add_trace(
            go.Scatter(
                x=cat_df["funding_display"],
                y=cat_df["y_jitter"],
                mode="markers",
                name=category,
                marker=dict(
                    size=cat_df["marker_size"].tolist(),
                    color=BUBBLE_COLORS[category],
                    opacity=0.7,
                    line=dict(width=1, color="white"),
                ),
                hovertemplate="%{text}<extra></extra>",
                text=hover_texts,
            )
        )

    # Dashed reference lines at key funding thresholds
    max_display = df["funding_display"].max()
    min_display = df["funding_display"].min()
    for threshold in [1_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]:
        if min_display <= threshold <= max_display:
            label = (
                f"€{threshold / 1_000_000:.0f}M"
                if threshold >= 1_000_000
                else f"€{threshold / 1_000:.0f}k"
            )
            fig.add_vline(
                x=threshold,
                line_dash="dash",
                line_color="gray",
                opacity=0.3,
                line_width=1,
                annotation_text=label,
                annotation_position="top",
                annotation_font_size=9,
            )

    fig.update_layout(
        title=dict(
            text="ECI Funding Amount vs Outcome",
            x=0.015,
            xanchor="left",
        ),
        xaxis=dict(
            title="Funding Amount (€)",
            type="log",
            tickvals=[200, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000],
            ticktext=["€0", "€500", "€1k", "€5k", "€10k", "€50k", "€100k", "€500k", "€1M", "€5M"],
            gridcolor="rgba(128,128,128,0.2)",
            showgrid=True,
        ),
        yaxis=dict(
            title="Outcome Category",
            tickmode="array",
            tickvals=list(range(len(present))),
            ticktext=present,
            gridcolor="rgba(128,128,128,0.1)",
            showgrid=True,
            range=[-0.5, len(present) - 0.5],
        ),
        hovermode="closest",
        margin=MARGIN,
        height=HEIGHT,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    return wrap_card(fig.to_html(**DIV_ARGS))
