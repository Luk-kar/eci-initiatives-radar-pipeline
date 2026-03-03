import pandas as pd
import plotly.graph_objects as go

from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card

ECI_THRESHOLD = 1_000_000


def _bar_color(signatures: float, max_signatures: float) -> str:
    """Gradient color per bar: dark-red→light-yellow below 1M, light-green→dark-green above."""
    if signatures >= ECI_THRESHOLD:
        # Light green → dark green as signatures grow beyond 1M
        ratio = min(
            (signatures - ECI_THRESHOLD) / max(max_signatures - ECI_THRESHOLD, 1), 1.0
        )
        r = int(184 - (184 - 60) * ratio)
        g = int(216 - (216 - 163) * ratio)
        b = int(127 - (127 - 113) * ratio)
    else:
        # Dark red → light yellow as signatures approach 1M
        ratio = signatures / ECI_THRESHOLD
        r = int(195 + (255 - 195) * ratio)
        g = int(66 + (244 - 66) * ratio)
        b = int(66 + (79 - 66) * ratio)
    return f"rgb({r},{g},{b})"


def generate_chart_top_10_signatures(df: pd.DataFrame) -> str:
    agg = (
        df.groupby("title", as_index=False)["signatures_numeric"]
        .sum()
        .nlargest(10, "signatures_numeric")
        .sort_values(
            "signatures_numeric", ascending=True
        )  # ascending → highest bar at top
    )

    max_sigs = agg["signatures_numeric"].max()
    colors = [_bar_color(s, max_sigs) for s in agg["signatures_numeric"]]

    fig = go.Figure(
        go.Bar(
            y=agg["title"],
            x=agg["signatures_numeric"],
            orientation="h",
            marker=dict(color=colors, line=dict(color="white", width=0.5)),
            hovertemplate="<b>%{y}</b><br>Signatures: %{x:,.0f}<extra></extra>",
        )
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

    fig.update_layout(
        title="Signatures Collected by Initiative",
        margin=MARGIN,
        height=HEIGHT,
        xaxis_title="Signatures",
        yaxis_title="",
        showlegend=False,
    )

    return wrap_card(fig.to_html(**DIV_ARGS))
