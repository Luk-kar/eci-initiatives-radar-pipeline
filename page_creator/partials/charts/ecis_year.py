"""Renders a stacked bar chart of ECI registration counts per year broken down by outcome status."""

import pandas as pd
import plotly.graph_objects as go

from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card
from page_creator.partials.charts.outcomes import STATUS_COLORS
from page_creator.partials.charts.utils import (
    hover_item_list,
    build_click_scroll_script,
    STATUS_SECTION_MAP,
)

# One category per STATUS_COLORS entry — order controls stacking order (bottom → top).
_CATEGORIES = [
    {"name": name, "statuses": {name}, "color": color}
    for name, color in reversed(STATUS_COLORS.items())
]


def generate_chart_ecis_year(df: pd.DataFrame) -> str:
    """
    Return an HTML card containing a stacked bar chart of ECIs per registration year by outcome.

    Each bar represents one registration year, stacked by outcome category in the
    order defined by ``_CATEGORIES``. Each segment's hover tooltip shows the
    category, year, count, and a bullet list of contributing initiative titles.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``registration_year``, and ``title`` columns.

    Returns:
        An HTML string wrapping the Plotly chart in a ``card`` div.
    """

    # Normalise raw CSV labels to match STATUS_COLORS keys.
    df = df.copy()

    years = sorted(df["registration_year"].dropna().unique())
    year_start, year_end = int(years[0]), int(years[-1])

    fig = go.Figure()

    for cat in _CATEGORIES:
        cat_df = df[df["current_status"].isin(cat["statuses"])]

        counts = (
            cat_df.groupby("registration_year")
            .size()
            .reindex(years, fill_value=0)
            .values
        )

        hover = [
            hover_item_list(
                cat_df[cat_df["registration_year"] == year]["title"].tolist()
            )
            for year in years
        ]

        fig.add_trace(
            go.Bar(
                x=years,
                y=counts,
                name=cat["name"],
                marker_color=cat["color"],
                customdata=hover,
                hovertemplate=(
                    f"<b>{cat['name']}</b><br>"
                    "<b>Year:</b> %{x}<br>"
                    "<b>Count:</b> %{y}<br><br>"
                    "<b>ECIs:</b><br>%{customdata}"
                    "<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title=dict(
            text=f"ECI Outcomes by Registration Year ({year_start} – {year_end})",
            x=0.015,
            xanchor="left",
        ),
        xaxis=dict(title="Registration Year", tickmode="linear", dtick=1),
        yaxis=dict(
            title="Number of Initiatives",
            domain=[0, 0.85 - 0.07],
        ),
        barmode="stack",
        margin=MARGIN,
        height=HEIGHT / 4 * 4,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.87 - 0.04,
            xanchor="right",
            x=1,
            traceorder="reversed",
        ),
    )

    return wrap_card(
        fig.to_html(
            **DIV_ARGS,
            post_script=build_click_scroll_script(
                STATUS_SECTION_MAP,
                point_key="data.name",  # trace name on the clicked bar segment
                strip_spaces=True,  # "Law Passed" → "LawPassed" for map lookup
            ),
        )
    )
