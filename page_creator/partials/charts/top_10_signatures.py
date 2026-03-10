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
    )


def _apply_top10_layout(fig: go.Figure) -> None:
    """Apply title, axis labels, and sizing to the top-10 bar chart."""
    fig.update_layout(
        title=dict(
            text="Top 10 Initiatives by Signatures (All-Time)",
            x=0.015,
            xanchor="left",
        ),
        margin=MARGIN,
        height=HEIGHT,
        xaxis_title="Signatures",
        yaxis=dict(title="", ticksuffix="   "),
        showlegend=False,
        clickmode="event",
    )


def _add_threshold_line(fig: go.Figure) -> None:
    """Draw a dashed green vertical line at the 1M signature threshold."""
    fig.add_vline(
        x=ECI_THRESHOLD,
        line_dash="dash",
        line_color="#3AB23F",
        line_width=2,
        annotation_text="1M threshold",
        annotation_position="top right",
        annotation_font_color="#3AB23F",
        annotation_font_size=13,
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
    """Return an HTML card containing a horizontal bar chart of the 10 highest-signature ECIs.

    Aggregates signatures by title, selects the top 10, and applies a
    red→yellow→green gradient based on distance from the 1M threshold. Each
    bar's hover tooltip shows year, signature count, countries threshold met,
    objective, and commission response. Clicking a bar opens the initiative's
    page in a new tab via an injected JS click handler.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``title``,
            ``signatures_collected``, ``signatures_threshold_met``,
            ``objective``, ``commission_answer_text``, ``url``, and
            ``registration_year`` columns.

    Returns:
        An HTML string wrapping the Plotly chart and its click handler script
        in a ``card`` div.
    """
    agg = _aggregate_top10(df)

    fig = go.Figure(_build_bar_trace(agg))
    _apply_top10_layout(fig)
    _add_threshold_line(fig)

    chart_html = fig.to_html(**{**DIV_ARGS, "div_id": _CHART_DIV_ID})
    return wrap_card(chart_html + _build_click_js())
