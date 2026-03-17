"""
Renders a donut chart of ECI initiative counts broken down by current outcome status.
"""

# Python
import pandas as pd
import plotly.graph_objects as go

# Local
from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card
from page_creator.partials.charts.utils import (
    hover_item_list,
    build_click_scroll_script,
    STATUS_SECTION_MAP,
)

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

STATUS_COLORS = {
    "Law Passed": "#3CA371",
    "Commission Engaged": "#9CCC65",
    "Rejected Legislation": "#F44336",
    "Awaiting Response": "#9E9E9E",
    "Collection Ongoing": "#3779BA",
    "Collection Unsuccessful": "#8B1111",
    "Withdrawn": "#4B4B4B",
}


_LABEL_ALIASES: dict[str, str] = {
    "Waiting for Response": "Awaiting Response",
}

DEFAULT_COLOR = "#757575"

MAX_TITLE_LEN = 40


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------


def _truncate_title(title: str, max_len: int = MAX_TITLE_LEN) -> str:
    """Truncate a title to ``max_len`` characters, appending '…' if cut."""

    return title if len(title) <= max_len else title[: max_len - 1] + "…"


def _normalise_statuses(df: pd.DataFrame) -> pd.DataFrame:
    """Replace aliased status labels and raise if any unrecognised values remain."""
    df = df.copy()
    df["current_status"] = df["current_status"].replace(_LABEL_ALIASES)
    unknown = set(df["current_status"].unique()) - STATUS_COLORS.keys()
    if unknown:
        raise ValueError(
            f"Unrecognised status values found in 'current_status': {sorted(unknown)}. "
            f"Add them to STATUS_COLORS or _LABEL_ALIASES."
        )
    return df


def _build_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate status counts, sort by STATUS_COLORS order, and attach percentages, colours, and hover lists."""
    counts = df["current_status"].value_counts().reset_index()
    counts.columns = ["current_status", "count"]

    status_order = list(STATUS_COLORS.keys())
    counts["_order"] = (
        counts["current_status"]
        .map({s: i for i, s in enumerate(status_order)})
        .fillna(len(status_order))
    )
    counts = counts.sort_values("_order").drop(columns="_order").reset_index(drop=True)

    total = counts["count"].sum()
    counts["percentage"] = (counts["count"] / total * 100).round(1)
    counts["color"] = counts["current_status"].map(
        lambda s: STATUS_COLORS.get(s, DEFAULT_COLOR)
    )
    counts["eci_list"] = counts["current_status"].apply(
        lambda s: hover_item_list(df[df["current_status"] == s]["title"].tolist())
    )
    return counts


def _build_pie_trace(counts: pd.DataFrame) -> go.Pie:
    """Construct the Plotly Pie trace from the aggregated counts DataFrame."""
    customdata = counts[["count", "percentage", "eci_list"]].values.tolist()
    return go.Pie(
        labels=counts["current_status"].str.replace(" ", "<br>"),
        values=counts["count"],
        hole=0.45,
        marker=dict(colors=counts["color"].tolist()),
        customdata=customdata,
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Count: %{customdata[0][0]}<br>"
            "Percentage: %{customdata[0][1]}%<br><br>"
            "<b>ECIs:</b><br>%{customdata[0][2]}"
            "<extra></extra>"
        ),
        textinfo="percent+label",
        textposition="inside",
        textfont=dict(size=11, color="white", family="Arial Black"),
        sort=False,
    )


def _apply_outcomes_layout(fig: go.Figure) -> None:
    """Apply title, sizing, and legend placement to the outcomes donut chart."""
    fig.update_layout(
        title="Initiatives by Current Status",
        margin=MARGIN,
        height=HEIGHT,
        width=500,
        showlegend=True,
        legend=dict(
            font=dict(size=12),
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
        ),
    )


# ------------------------------------------------------------------------------
# Chart
# ------------------------------------------------------------------------------


def generate_chart_outcomes(df: pd.DataFrame) -> str:
    """Return an HTML card containing a donut chart of initiatives grouped by outcome status.

    Slices follow the order defined in ``STATUS_COLORS``; statuses not present
    in ``STATUS_COLORS`` after alias normalisation raise a ``ValueError``.
    Each slice's hover tooltip shows count, percentage, and a bullet list of
    up to ``MAX_HOVER_ITEMS`` contributing initiative titles.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``
            and ``title`` columns. All ``current_status`` values must be present
            in ``STATUS_COLORS`` after ``_LABEL_ALIASES`` normalisation.

    Returns:
        An HTML string wrapping the Plotly chart in a ``card bottom-col`` div.

    Raises:
        ValueError: If any ``current_status`` value is not found in ``STATUS_COLORS``.
    """
    df = _normalise_statuses(df)
    counts = _build_counts(df)

    fig = go.Figure(_build_pie_trace(counts))
    _apply_outcomes_layout(fig)

    html_content = fig.to_html(
        **DIV_ARGS,
        post_script=build_click_scroll_script(
            STATUS_SECTION_MAP,
            point_key="label",
            strip_br=True,
        ),
    )

    return wrap_card(html_content, extra_class="bottom-col")
