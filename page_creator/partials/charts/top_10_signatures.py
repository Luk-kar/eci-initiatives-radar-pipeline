import textwrap

import pandas as pd
import plotly.graph_objects as go

from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card

ECI_THRESHOLD = 1_000_000
_WRAP_WIDTH = 60
_CHART_DIV_ID = "chart-top10-signatures"

_WRAP_WIDTH = 60
_MAX_LINES = 6


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


def _hover_wrap(text: str) -> str:
    """Break long text into <br>-separated lines for Plotly hover tooltips.
    Truncates to max_lines and appends '…' if the text exceeds the limit."""

    lines = textwrap.wrap(str(text), width=_WRAP_WIDTH)

    if len(lines) > _MAX_LINES:
        lines = lines[:_MAX_LINES]
        lines[-1] = lines[-1].rstrip() + "…"

    return "<br>".join(lines)


def generate_chart_top_10_signatures(df: pd.DataFrame) -> str:
    agg = (
        df.groupby("title", as_index=False)
        .agg(
            signatures_collected=("signatures_collected", "sum"),
            signatures_threshold_met=("signatures_threshold_met", "first"),
            objective=("objective", "first"),
            commission_answer_text=("commission_answer_text", "first"),
            url=("url", "first"),
            registration_year=("registration_year", "first"),  # ← ADD THIS
        )
        .nlargest(10, "signatures_collected")
        .sort_values("signatures_collected", ascending=True)
    )

    agg["objective"] = agg["objective"].apply(_hover_wrap)
    agg["commission_answer_text"] = agg["commission_answer_text"].apply(_hover_wrap)
    agg["registration_year",] = agg["registration_year"].apply(_hover_wrap)

    max_sigs = agg["signatures_collected"].max()
    colors = [_bar_color(s, max_sigs) for s in agg["signatures_collected"]]

    # customdata: [0] threshold_met  [1] objective  [2] commission_answer_text  [3] url
    customdata = agg[
        [
            "signatures_threshold_met",
            "objective",
            "commission_answer_text",
            "url",
            "registration_year",
        ]
    ].values

    fig = go.Figure(
        go.Bar(
            y=agg["title"],
            x=agg["signatures_collected"],
            orientation="h",
            marker=dict(color=colors, line=dict(color="white", width=0.5)),
            customdata=customdata,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "<b>Year:</b> %{customdata[4]}<br><br>"
                "<b>Signatures:</b> %{x:,.0f}<br>"
                "<b>Countries Threshold Met:</b> %{customdata[0]}/27<br><br>"
                "<b>Objective:</b><br>%{customdata[1]}<br><br>"
                "<b>Commission Response:</b><br>%{customdata[2]}<br><br>"
                "<i>🔗 Click to open initiative page</i>"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=dict(
            text="Top 10 Initiatives by Signatures (All-Time)",
            x=0.015,
            xanchor="left",
        ),
        margin=MARGIN,
        height=HEIGHT,
        xaxis_title="Signatures",
        yaxis=dict(
            title="",
            ticksuffix="   ",
        ),
        yaxis_title="",
        showlegend=False,
        clickmode="event",
    )

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

    chart_html = fig.to_html(**{**DIV_ARGS, "div_id": _CHART_DIV_ID})

    click_js = f"""
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
</script>
"""

    return wrap_card(chart_html + click_js)
