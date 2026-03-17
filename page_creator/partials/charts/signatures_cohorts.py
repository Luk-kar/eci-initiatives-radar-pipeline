"""Renders a colour-coded histogram of ECI signature counts split at the 1M threshold."""

from typing import Callable

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card
from page_creator.partials.styles.colors import kpi_colors

ECI_THRESHOLD = 1_000_000
NUM_BINS = 50
MAX_HOVER_ITEMS = 15


class _BinGroup:
    """Precomputed data for one histogram group (below or above threshold)."""

    def __init__(
        self,
        name: str,
        centers: np.ndarray,
        counts: np.ndarray,
        widths: np.ndarray,
        colors: list[str],
        hover: list[str],
    ) -> None:
        self.name = name
        self.centers = centers
        self.counts = counts
        self.widths = widths
        self.colors = colors
        self.hover = hover


def _get_bin_ecis(df: pd.DataFrame, bin_start: float, bin_end: float) -> str:
    """
    Return a ``<br>``-joined list of ECI titles whose signatures fall
    within the given bin range.
    """

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


def _filter_valid_signatures(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with missing signature counts."""
    return df[df["signatures_collected"].notna()].copy()


def _split_bins(max_val: float) -> tuple[np.ndarray, np.ndarray]:
    """Split ``NUM_BINS`` evenly spaced edges into below- and above-threshold groups."""
    all_bins = np.linspace(0, max_val, NUM_BINS + 1)
    return all_bins[all_bins < ECI_THRESHOLD], all_bins[all_bins >= ECI_THRESHOLD]


def _colorize_below(centers: np.ndarray) -> list[str]:
    """Map below-threshold bin centers to a red→yellow gradient."""
    colors = []
    for center in centers:
        ratio = center / ECI_THRESHOLD
        r = int(195 + (255 - 195) * ratio)
        g = int(66 + (244 - 66) * ratio)
        b = int(66 + (79 - 66) * ratio)
        colors.append(f"rgb({r},{g},{b})")
    return colors


def _colorize_above(centers: np.ndarray) -> list[str]:
    """Map above-threshold bin centers to a light→dark green gradient."""
    colors = []
    for center in centers:
        ratio = min((center - ECI_THRESHOLD) / ECI_THRESHOLD, 1.0)
        r = int(184 - (184 - 60) * ratio)
        g = int(216 - (216 - 163) * ratio)
        b = int(127 - (127 - 113) * ratio)
        colors.append(f"rgb({r},{g},{b})")
    return colors


def _build_bin_group(
    sigs: pd.DataFrame,
    bins: np.ndarray,
    name: str,
    colorize: Callable[[np.ndarray], list[str]],
) -> _BinGroup:
    """Compute histogram counts, centers, widths, colors, and hover texts for one bin group."""
    counts, edges = np.histogram(sigs["signatures_collected"], bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    return _BinGroup(
        name=name,
        centers=centers,
        counts=counts,
        widths=np.diff(edges),
        colors=colorize(centers),
        hover=[
            _get_bin_ecis(sigs, edges[i], edges[i + 1]) for i in range(len(edges) - 1)
        ],
    )


def _add_bar_trace(fig: go.Figure, group: _BinGroup) -> None:
    """Append a single colour-coded Bar trace to the figure."""
    fig.add_trace(
        go.Bar(
            x=group.centers,
            y=group.counts,
            name=group.name,
            marker=dict(color=group.colors, line=dict(color="white", width=0.5)),
            width=group.widths,
            customdata=group.hover,
            hovertemplate=(
                "<b>Signatures Range:</b> %{x:,.0f}<br>"
                "<b>Count:</b> %{y}<br><br>"
                "<b>ECIs:</b><br>%{customdata}"
                "<extra></extra>"
            ),
        )
    )


def _add_threshold_line(fig: go.Figure) -> None:
    """Draw a dashed green vertical line at the 1M signature threshold."""
    fig.add_vline(
        x=ECI_THRESHOLD,
        line_dash="dash",
        line_color=kpi_colors.threshold_line,
        line_width=3,
        annotation_text="1M Threshold",
        annotation_position="top right",
        annotation_font_size=13,
        annotation_font_color=kpi_colors.threshold_line,
    )


def _apply_layout(fig: go.Figure) -> None:
    """Apply axis labels, sizing, and legend configuration to the figure."""
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


def generate_chart_signatures_cohorts(df: pd.DataFrame) -> str:
    """Return an HTML card containing a bar chart of ECI signature-count distribution.

    Bins all initiatives into ``NUM_BINS`` equally spaced buckets across the full
    signature range, then renders two colour-coded trace groups — a red-to-yellow
    gradient below the 1M threshold and a green gradient above it. A dashed
    vertical line marks the threshold. Each bar's hover tooltip lists up to
    ``MAX_HOVER_ITEMS`` initiative titles within that bin.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``signatures_collected``
            and ``title`` columns; rows with ``NaN`` signatures are silently dropped.

    Returns:
        An HTML string wrapping the Plotly chart in a ``card bottom-col`` div.
    """
    sigs = _filter_valid_signatures(df)
    below_bins, above_bins = _split_bins(sigs["signatures_collected"].max())

    below = _build_bin_group(
        sigs[sigs["signatures_collected"] < ECI_THRESHOLD],
        below_bins,
        "Below 1M",
        _colorize_below,
    )
    above = _build_bin_group(
        sigs[sigs["signatures_collected"] >= ECI_THRESHOLD],
        above_bins,
        "Above 1M",
        _colorize_above,
    )

    fig = go.Figure()
    _add_bar_trace(fig, below)
    _add_bar_trace(fig, above)
    _add_threshold_line(fig)
    _apply_layout(fig)

    return wrap_card(fig.to_html(**DIV_ARGS), extra_class="bottom-col")
