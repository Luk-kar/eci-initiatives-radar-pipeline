import numpy as np
import pandas as pd
import plotly.graph_objects as go

from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card

ECI_THRESHOLD = 1_000_000
NUM_BINS = 50
MAX_HOVER_ITEMS = 15


def _get_bin_ecis(df: pd.DataFrame, bin_start: float, bin_end: float) -> str:
    titles = df[
        (df["signatures_collected"] >= bin_start)
        & (df["signatures_collected"] <= bin_end)
    ]["title"].tolist()

    if not titles:
        return "No ECIs"

    items = [f"• {t}" for t in titles[:MAX_HOVER_ITEMS]]
    result = "<br>".join(items)
    if len(titles) > MAX_HOVER_ITEMS:
        result += f"<br><i>... (and {len(titles) - MAX_HOVER_ITEMS} more)</i>"
    return result


def generate_chart_signatures_cohorts(df: pd.DataFrame) -> str:
    sigs = df[df["signatures_collected"].notna()].copy()

    bins = np.linspace(0, sigs["signatures_collected"].max(), NUM_BINS + 1)
    below_bins = bins[bins < ECI_THRESHOLD]
    above_bins = bins[bins >= ECI_THRESHOLD]

    hist_below, edges_below = np.histogram(
        sigs[sigs["signatures_collected"] < ECI_THRESHOLD]["signatures_collected"],
        bins=below_bins,
    )
    hist_above, edges_above = np.histogram(
        sigs[sigs["signatures_collected"] >= ECI_THRESHOLD]["signatures_collected"],
        bins=above_bins,
    )

    centers_below = (edges_below[:-1] + edges_below[1:]) / 2
    centers_above = (edges_above[:-1] + edges_above[1:]) / 2

    eci_lists_below = [
        _get_bin_ecis(sigs, edges_below[i], edges_below[i + 1])
        for i in range(len(edges_below) - 1)
    ]
    eci_lists_above = [
        _get_bin_ecis(sigs, edges_above[i], edges_above[i + 1])
        for i in range(len(edges_above) - 1)
    ]

    colors_below = []
    for center in centers_below:
        ratio = center / ECI_THRESHOLD
        r = int(195 + (255 - 195) * ratio)
        g = int(66 + (244 - 66) * ratio)
        b = int(66 + (79 - 66) * ratio)
        colors_below.append(f"rgb({r},{g},{b})")

    colors_above = []
    for center in centers_above:
        ratio = min((center - ECI_THRESHOLD) / ECI_THRESHOLD, 1.0)
        r = int(184 - (184 - 60) * ratio)
        g = int(216 - (216 - 163) * ratio)
        b = int(127 - (127 - 113) * ratio)
        colors_above.append(f"rgb({r},{g},{b})")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=centers_below,
            y=hist_below,
            name="Below 1M",
            marker=dict(color=colors_below, line=dict(color="white", width=0.5)),
            width=np.diff(edges_below),
            customdata=eci_lists_below,
            hovertemplate=(
                "<b>Signatures Range:</b> %{x:,.0f}<br>"
                "<b>Count:</b> %{y}<br><br>"
                "<b>ECIs:</b><br>%{customdata}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Bar(
            x=centers_above,
            y=hist_above,
            name="Above 1M",
            marker=dict(color=colors_above, line=dict(color="white", width=0.5)),
            width=np.diff(edges_above),
            customdata=eci_lists_above,
            hovertemplate=(
                "<b>Signatures Range:</b> %{x:,.0f}<br>"
                "<b>Count:</b> %{y}<br><br>"
                "<b>ECIs:</b><br>%{customdata}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_vline(
        x=ECI_THRESHOLD,
        line_dash="dash",
        line_color="#3AB23F",
        line_width=3,
        annotation_text="1M Threshold",
        annotation_position="top right",
        annotation_font_size=13,
        annotation_font_color="#3AB23F",
    )

    fig.update_layout(
        title="Distribution of Signature Counts",
        xaxis_title="Signatures Collected",
        yaxis_title="Number of Initiatives",
        margin=MARGIN,
        height=HEIGHT,
        width=620,
        showlegend=True,
        bargap=0.05,
        legend=dict(font=dict(size=13)),
    )

    return wrap_card(fig.to_html(**DIV_ARGS), extra_class="bottom-col")
