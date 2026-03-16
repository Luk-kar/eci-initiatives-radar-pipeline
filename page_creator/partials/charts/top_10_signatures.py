"""Renders a horizontal bar chart of the top 10 ECI initiatives by total signatures collected."""

# Python
import pandas as pd
import plotly.graph_objects as go

# Local
from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card
from page_creator.partials.charts.utils import hover_wrap

ECI_THRESHOLD = 1_000_000
_CHART_DIV_ID = "chart-top10-signatures"

_HOVERTEMPLATE = (
    "<b>%{y}</b><br>"
    "<b>Year:</b> %{customdata[4]}<br><br>"
    "<b>Signatures:</b> %{x:,.0f}<br>"
    "<b>Countries Threshold Met:</b> %{customdata[0]}/27<br><br>"
    "<b>Objective:</b><br>%{customdata[1]}<br><br>"
    "<b>Commission Response:</b><br>%{customdata[2]}<br><br>"
    "<i>🔗 Click to open initiative page</i>"
    "<extra></extra>"
)

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
    """Aggregate by title, select the top 10 by signatures, and wrap long text fields for hover."""
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
    agg["commission_answer_text"] = agg["commission_answer_text"].apply(hover_wrap)
    return agg


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
        hovertemplate=_HOVERTEMPLATE,
        showlegend=False,
    )


def _apply_top10_layout(fig: go.Figure) -> None:
    """Apply title, axis labels, sizing, and legend to the top-10 bar chart."""
    fig.update_layout(
        title=dict(
            text="Top 10 Initiatives by Signatures (All-Time)",
            x=0.015,
            xanchor="left",
        ),
        margin=MARGIN,
        height=HEIGHT,
        xaxis_title="Signatures",
        yaxis=dict(title="", ticksuffix=" "),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=11),
        ),
        clickmode="event",
    )


def _add_threshold_line(fig: go.Figure) -> None:
    """Draw a dashed green vertical line at the 1M signature threshold."""
    fig.add_vline(
        x=ECI_THRESHOLD,
        line_dash="dash",
        line_color="#3AB23F",
        line_width=3,
    )


def _add_status_markers(fig: go.Figure, agg: pd.DataFrame) -> None:
    """Add a scatter marker at the end of each bar indicating the initiative's current status."""
    groups: dict[str, list[dict]] = {status: [] for status in STATUS_MARKERS}

    for _, row in agg.iterrows():
        status = row.get("current_status")
        if status in groups:
            groups[status].append(
                {
                    "x": row["signatures_collected"],
                    "y": row["title"],
                    "url": row["url"],
                }
            )

    for status, data in groups.items():
        if not data:
            continue

        cfg = STATUS_MARKERS[status]
        fig.add_trace(
            go.Scatter(
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
                customdata=[
                    [None, None, None, d["url"]] for d in data
                ],  # ← [3] matches bar's URL index
                hovertemplate=(
                    f"<b>%{{y}}</b><br>"
                    f"Status: {status}<br>"
                    f"Signatures: %{{x:,.0f}}<extra></extra>"
                ),
            )
        )


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


def generate_chart_top_10_signatures(df: pd.DataFrame) -> str:
    """Build and return the top-10 signatures chart as an HTML div string."""
    agg = _aggregate_top10(df)

    fig = go.Figure(_build_bar_trace(agg))
    _apply_top10_layout(fig)
    _add_threshold_line(fig)
    _add_status_markers(fig, agg)

    chart_html = fig.to_html(**{**DIV_ARGS, "div_id": _CHART_DIV_ID})
    return wrap_card(chart_html + _build_click_js())
