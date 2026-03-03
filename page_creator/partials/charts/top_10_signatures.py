import textwrap

import pandas as pd
import plotly.graph_objects as go

from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card

ECI_THRESHOLD = 1_000_000
_WRAP_WIDTH = 60


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


def _hover_wrap(text: str, width: int = _WRAP_WIDTH) -> str:
    """Break long text into <br>-separated lines for Plotly hover tooltips."""
    lines = textwrap.wrap(str(text), width=width)
    return "<br>".join(lines)


def generate_chart_top_10_signatures(df: pd.DataFrame) -> str:
    agg = (
        df.groupby("title", as_index=False)
        .agg(
            signatures_numeric=("signatures_numeric", "sum"),
            signatures_threshold_met=("signatures_threshold_met", "first"),
            objective=("objective", "first"),
            commission_answer_text=("commission_answer_text", "first"),
        )
        .nlargest(10, "signatures_numeric")
        .sort_values("signatures_numeric", ascending=True)
    )

    agg["objective"] = agg["objective"].apply(_hover_wrap)
    agg["commission_answer_text"] = agg["commission_answer_text"].apply(_hover_wrap)

    max_sigs = agg["signatures_numeric"].max()
    colors = [_bar_color(s, max_sigs) for s in agg["signatures_numeric"]]

    # customdata columns: [0] threshold_met  [1] objective  [2] commission_answer_text
    customdata = agg[
        ["signatures_threshold_met", "objective", "commission_answer_text"]
    ].values

    fig = go.Figure(
        go.Bar(
            y=agg["title"],
            x=agg["signatures_numeric"],
            orientation="h",
            marker=dict(color=colors, line=dict(color="white", width=0.5)),
            customdata=customdata,
            hovertemplate=(
                "<b>%{y}</b><br><br>"
                "<b>Signatures:</b> %{x:,.0f}<br>"
                "<b>Countries Threshold Met:</b> %{customdata[0]}/7<br><br>"
                "<b>Objective:</b><br>%{customdata[1]}<br><br>"
                "<b>Commission Response:</b><br>%{customdata[2]}"
                "<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        title="Signatures Collected by Initiative",
        margin=MARGIN,
        height=HEIGHT,
        xaxis_title="Signatures",
        yaxis_title="",
        showlegend=False,
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

    return wrap_card(fig.to_html(**DIV_ARGS))
