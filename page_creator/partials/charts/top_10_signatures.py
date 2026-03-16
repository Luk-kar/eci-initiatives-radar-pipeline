"""Renders a horizontal bar chart of the top 10 ECI initiatives by total signatures collected."""

# Python
import pandas as pd
import plotly.graph_objects as go

# Local
from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card
from page_creator.partials.charts.utils import hover_wrap


# ── Constants ──────────────────────────────────────────────────────────────

ECI_THRESHOLD = 1_000_000
_CHART_DIV_ID = "chart-top10-signatures"

# ── Hover templates ────────────────────────────────────────────────────────

_HOVER_BASE = (
    "<b>%{y}</b><br>"
    "<b>Year:</b> %{customdata[4]}<br><br>"
    "<b>Signatures:</b> %{x:,.0f}<br>"
    "<b>Countries Threshold Met:</b> %{customdata[0]}/27<br><br>"
)

_HOVER_FOOTER = "<i>🔗 Click to open initiative page</i>" "<extra></extra>"

_HOVERTEMPLATE_BAR = (
    _HOVER_BASE + "<b>🎯 Objective:</b><br>%{customdata[1]}<br><br>" + _HOVER_FOOTER
)

_HOVERTEMPLATE_SYMBOL = (
    _HOVER_BASE
    + "<b>📬 Commission Response (%{customdata[5]}):</b><br>%{customdata[2]}<br><br>"
    + _HOVER_FOOTER
)

# ── Status marker config ───────────────────────────────────────────────────

STATUS_MARKERS = {
    "Commission Engaged": {
        "symbol": "triangle-right",
        "color": "#9CCC65",
        "label": "Commission Engaged",
    },
    "Rejected Legislation": {
        "symbol": "x",
        "color": "#F44336",
        "label": "Rejected Legislation",
    },
    "Collection Unsuccessful": {
        "symbol": "x",
        "color": "#8B1111",
        "label": "Collection Unsuccessful",
    },
    "Withdrawn": {
        "symbol": "x",
        "color": "#4B4B4B",
        "label": "Withdrawn",
    },
    "Waiting for Response": {
        "symbol": "hourglass",
        "color": "#9E9E9E",
        "label": "Waiting for Response",
    },
    "Law Passed": {
        "symbol": "star",
        "color": "#3CA371",
        "label": "Law Passed",
    },
    "Collection Ongoing": {
        "symbol": "triangle-right",
        "color": "#F5A623",
        "label": "Collection Ongoing",
    },
}

_COMMISSION_ANSWER_FALLBACK = {
    "Collection Unsuccessful": "<i>Did not reach the required signatures.</i>",
    "Withdrawn": "<i>Withdrawn by the organisers.</i>",
    "Waiting for Response": "<i>Commission response pending.</i>",
    "Collection Ongoing": "<i>Signatures still being collected.</i>",
}

# ── Data preparation ───────────────────────────────────────────────────────


def _bar_color(signatures: float, max_signatures: float) -> str:
    """Gradient color per bar: dark-red→light-yellow below 1M, light-green→dark-green above."""

    if signatures >= ECI_THRESHOLD:
        ratio = min(
            (signatures - ECI_THRESHOLD) / max(max_signatures - ECI_THRESHOLD, 1), 1.0
        )
        r = int(184 - (184 - 60) * ratio)
        g = int(216 - (216 - 163) * ratio)
        b = int(127 - (127 - 113) * ratio)
    else:
        ratio = signatures / ECI_THRESHOLD
        r = int(195 + (255 - 195) * ratio)
        g = int(66 + (244 - 66) * ratio)
        b = int(66 + (79 - 66) * ratio)
    return f"rgb({r},{g},{b})"


def _aggregate_top10(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate by title,
    select the top 10 by signatures,
    and wrap long text fields for hover.
    """

    agg = (
        df.groupby("title", as_index=False)
        .agg(
            signatures_collected=("signatures_collected", "sum"),
            signatures_threshold_met=("signatures_threshold_met", "first"),
            objective=("objective", "first"),
            commission_answer_text=("commission_answer_text", "first"),
            url=("url", "first"),
            registration_year=("registration_year", "first"),
            current_status=("current_status", "first"),
        )
        .nlargest(10, "signatures_collected")
        .sort_values("signatures_collected", ascending=True)
    )

    agg["objective"] = agg["objective"].apply(hover_wrap)

    agg["commission_answer_text"] = agg.apply(
        lambda row: hover_wrap(
            row["commission_answer_text"]
            if pd.notna(row["commission_answer_text"])
            else _COMMISSION_ANSWER_FALLBACK.get(row["current_status"])
        ),
        axis=1,
    )

    return agg


# ── Bar trace ──────────────────────────────────────────────────────────────


def _build_bar_trace(agg: pd.DataFrame) -> go.Bar:
    """Construct the colour-graded horizontal Bar trace with customdata and hovertemplate."""

    max_sigs = agg["signatures_collected"].max()
    colors = [_bar_color(s, max_sigs) for s in agg["signatures_collected"]]
    customdata = agg[
        [
            "signatures_threshold_met",
            "objective",
            "commission_answer_text",
            "url",
            "registration_year",
        ]
    ].values

    return go.Bar(
        y=agg["title"],
        x=agg["signatures_collected"],
        orientation="h",
        marker=dict(color=colors, line=dict(color="white", width=0.5)),
        customdata=customdata,
        hovertemplate=_HOVERTEMPLATE_BAR,
        showlegend=False,
    )


# ── Layout ─────────────────────────────────────────────────────────────────


def _apply_top10_title(fig: go.Figure) -> None:
    """Set the chart title."""
    fig.update_layout(
        title=dict(
            text="Top 10 Initiatives by Signatures (All-Time)",
            x=0.015,
            xanchor="left",
        ),
    )


def _apply_top10_axes(fig: go.Figure) -> None:
    """Set axis labels and tick formatting."""
    fig.update_layout(
        xaxis_title="Signatures",
        yaxis=dict(title="", ticksuffix=" "),
    )


def _apply_top10_legend(fig: go.Figure) -> None:
    """Configure legend visibility and positioning."""
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=11),
        ),
    )


def _apply_top10_layout(fig: go.Figure) -> None:
    """Apply title, axes, sizing, legend, and interaction settings to the top-10 bar chart."""
    _apply_top10_title(fig)
    _apply_top10_axes(fig)
    _apply_top10_legend(fig)
    fig.update_layout(
        margin=MARGIN,
        height=HEIGHT,
        clickmode="event",
    )


# ── Threshold line ─────────────────────────────────────────────────────────


def _add_threshold_line(fig: go.Figure) -> None:
    """Draw a dashed green vertical line at the 1M signature threshold."""

    fig.add_vline(
        x=ECI_THRESHOLD,
        line_dash="dash",
        line_color="#3AB23F",
        line_width=3,
    )


# ── Status markers ─────────────────────────────────────────────────────────


def _group_markers_by_status(agg: pd.DataFrame) -> dict[str, list[dict]]:
    """Group aggregated rows by current_status for marker rendering."""

    groups: dict[str, list[dict]] = {status: [] for status in STATUS_MARKERS}

    for _, row in agg.iterrows():
        status = row.get("current_status")

        if status in groups:

            groups[status].append(
                {
                    "x": row["signatures_collected"],
                    "y": row["title"],
                    "url": row["url"],
                    "signatures_threshold_met": row["signatures_threshold_met"],  # [0]
                    "commission_answer_text": row["commission_answer_text"],  # [2]
                    "registration_year": row["registration_year"],  # [4]
                }
            )

    return groups


def _build_marker_customdata(data: list[dict], status: str) -> list[list]:
    """Build the customdata array for a single status scatter trace."""

    return [
        [
            d["signatures_threshold_met"],  # [0]
            None,  # [1]
            d["commission_answer_text"],  # [2]
            d["url"],  # [3]
            d["registration_year"],  # [4]
            status,  # [5] ← status label for hover
        ]
        for d in data
    ]


def _build_status_scatter(status: str, data: list[dict]) -> go.Scatter:
    """Construct a single Scatter trace for one status group."""

    cfg = STATUS_MARKERS[status]
    return go.Scatter(
        x=[d["x"] for d in data],
        y=[d["y"] for d in data],
        mode="markers",
        marker=dict(
            symbol=cfg["symbol"],
            size=14,
            color=cfg["color"],
            line=dict(width=2, color="white"),
        ),
        name=cfg["label"],
        legendgroup=f"status_{status.lower().replace(' ', '_')}",
        showlegend=True,
        customdata=_build_marker_customdata(data, status),
        hovertemplate=_HOVERTEMPLATE_SYMBOL,
    )


def _add_status_markers(fig: go.Figure, agg: pd.DataFrame) -> None:
    """Add a scatter marker at the end of each bar indicating the initiative's current status."""

    groups = _group_markers_by_status(agg)

    for status, data in groups.items():

        if not data:
            continue

        fig.add_trace(_build_status_scatter(status, data))


# ── Click JS ───────────────────────────────────────────────────────────────


def _build_click_js() -> str:
    """Return the inline script and style that add pointer cursor and URL-open on bar click."""

    return f"""
<style>
  #{_CHART_DIV_ID} .bars path {{ cursor: pointer !important; }}
</style>
<script>
(function () {{
  var el = document.getElementById("{_CHART_DIV_ID}");
  var drag = el.querySelector(".nsewdrag");
  el.on("plotly_hover", function () {{
    if (drag) drag.style.cursor = "pointer";
  }});
  el.on("plotly_unhover", function () {{
    if (drag) drag.style.cursor = "default";
  }});
  el.on("plotly_click", function (data) {{
    var url = data.points[0].customdata[3];
    if (url) window.open(url, "_blank", "noopener,noreferrer");
  }});
}})();
</script>"""


# ── Entry point ────────────────────────────────────────────────────────────


def generate_chart_top_10_signatures(df: pd.DataFrame) -> str:
    """Build and return the top-10 signatures chart as an HTML div string."""

    agg = _aggregate_top10(df)

    fig = go.Figure(_build_bar_trace(agg))
    _apply_top10_layout(fig)
    _add_threshold_line(fig)
    _add_status_markers(fig, agg)

    chart_html = fig.to_html(**{**DIV_ARGS, "div_id": _CHART_DIV_ID})
    return wrap_card(chart_html + _build_click_js())
