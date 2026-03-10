import numpy as np
import pandas as pd
import plotly.graph_objects as go

from page_creator.config import DIV_ARGS, HEIGHT, MARGIN
from page_creator.partials.charts.outcomes import STATUS_COLORS
from page_creator.utils import wrap_card


# ── Colour scheme & category order ───────────────────────────────────────────
BUBBLE_COLORS: dict[str, str] = {
    "Collection Unsuccessful": STATUS_COLORS["Collection Unsuccessful"],  # dark red
    "Collection Ongoing": STATUS_COLORS["Collection Ongoing"],  # amber / orange
    "Awaiting Response": STATUS_COLORS["Awaiting Response"],  # medium grey
    "Rejected Legislation": STATUS_COLORS["Rejected Legislation"],  # red
    "Commission Engaged": STATUS_COLORS["Commission Engaged"],  # light green
    "Law Passed": STATUS_COLORS["Law Passed"],  # teal green
}

_CATEGORY_ORDER = list(BUBBLE_COLORS.keys())

_STATUS_ALIASES: dict[str, str] = {
    "Waiting for Response": "Awaiting Response",
    "Withdrawn": "Collection Unsuccessful",
}

_LOG_ZERO_DISPLAY = 200


# ── Helpers ───────────────────────────────────────────────────────────────────
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


def _prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise statuses, parse funding, drop unknown rows."""

    df = df.copy()
    df["current_status"] = df["current_status"].replace(_STATUS_ALIASES)
    df["bubble_category"] = df["current_status"]
    df = df[df["bubble_category"].isin(BUBBLE_COLORS)].reset_index(drop=True)

    df["funding_numeric"] = df["funding_total"].apply(_parse_funding)
    df["funding_display"] = df["funding_numeric"].apply(
        lambda v: _LOG_ZERO_DISPLAY if v == 0.0 else v
    )
    df["has_zero_funding"] = df["funding_numeric"] == 0.0
    return df


def _add_jitter(df: pd.DataFrame, present: list[str]) -> pd.DataFrame:
    """Assign integer y positions and add uniform jitter for visual separation."""

    cat_index = {c: i for i, c in enumerate(present)}
    df["y_pos"] = df["bubble_category"].map(cat_index)
    rng = np.random.default_rng(42)
    df["y_jitter"] = df["y_pos"] + rng.uniform(-0.15, 0.15, len(df))
    return df


def _compute_marker_sizes(df: pd.DataFrame) -> pd.DataFrame:
    """Log-normalise funding to marker sizes in [8, 43]."""

    log_f = np.log10(df["funding_display"])
    span = log_f.max() - log_f.min()
    df["marker_size"] = (log_f - log_f.min()) / span * 35 + 8 if span > 0 else 20
    df["marker_size"] = df["marker_size"].fillna(15).clip(lower=5, upper=50)
    return df


def _build_hover(row: pd.Series) -> str:
    """Format a single bubble's hover tooltip with title, funding, and status."""

    funding_label = (
        "€0 (No funding data)"
        if row["has_zero_funding"]
        else f"€{row['funding_numeric']:,.0f}"
    )
    return (
        f"<b>{str(row['title'])[:65]}</b><br>"
        f"Funding: {funding_label}<br>"
        f"Status: {row['current_status']}"
    )


def _add_traces(fig: go.Figure, df: pd.DataFrame, present: list[str]) -> None:
    """Add one Scatter trace per category, sized and coloured by funding amount."""

    for category in present:
        cat_df = df[df["bubble_category"] == category]
        hover_texts = [_build_hover(row) for _, row in cat_df.iterrows()]

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


def _add_threshold_lines(fig: go.Figure, df: pd.DataFrame) -> None:
    """Draw dashed vertical reference lines at key funding thresholds."""

    min_display = df["funding_display"].min()
    max_display = df["funding_display"].max()

    for threshold in [1_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]:
        if not (min_display <= threshold <= max_display):
            continue
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


def _apply_layout(fig: go.Figure, present: list[str], title_amount: str) -> None:
    """Apply axis configuration, legend placement, and title to the figure."""

    fig.update_layout(
        title=dict(
            text=f"ECI Initiative Funding ({title_amount} total) by Final Outcome",
            x=0.015,
            xanchor="left",
        ),
        xaxis=dict(
            title="Funding Amount (€)",
            type="log",
            tickvals=[
                200,
                500,
                1_000,
                5_000,
                10_000,
                50_000,
                100_000,
                500_000,
                1_000_000,
                5_000_000,
            ],
            ticktext=[
                "€0",
                "€500",
                "€1k",
                "€5k",
                "€10k",
                "€50k",
                "€100k",
                "€500k",
                "€1M",
                "€5M",
            ],
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
            domain=[0, 0.9],
        ),
        hovermode="closest",
        margin=MARGIN,
        height=HEIGHT / 4 * 5,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.92,
            xanchor="right",
            x=1,
            traceorder="reversed",
        ),
    )


def _present_categories(df: pd.DataFrame) -> list[str]:
    """Return category order filtered to those actually present in the data."""
    return [c for c in _CATEGORY_ORDER if c in df["bubble_category"].values]


def _format_amount(value: float) -> str:
    """Round a euro amount to the nearest K, M, or B — omits decimal if whole."""
    for threshold, suffix in [(1_000_000_000, "B"), (1_000_000, "M"), (1_000, "K")]:
        if value >= threshold:
            formatted = f"{value / threshold:.1f}".rstrip("0").rstrip(".")
            return f"€{formatted}{suffix}"
    return f"€{value:.0f}"


# ── Public entry point ────────────────────────────────────────────────────────
def generate_chart_bubble_finance_plot(df: pd.DataFrame) -> str:
    df = _prepare_dataframe(df)
    present = _present_categories(df)
    df = _add_jitter(df, present)
    df = _compute_marker_sizes(df)

    total_eur = df["funding_numeric"].sum()
    title_amount = _format_amount(df["funding_numeric"].sum())

    fig = go.Figure()
    _add_traces(fig, df, present)
    _add_threshold_lines(fig, df)
    _apply_layout(fig, present, title_amount)

    return wrap_card(fig.to_html(**DIV_ARGS))
