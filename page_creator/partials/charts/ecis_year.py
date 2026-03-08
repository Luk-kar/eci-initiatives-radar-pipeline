import pandas as pd
import plotly.graph_objects as go

from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card

MAX_HOVER_ITEMS = 10

# Current status values grouped into four outcome buckets.
# Order here controls stacking order (bottom → top).
_CATEGORIES = [
    {
        "name": "Collection Failed",
        "statuses": {"Collection Unsuccessful", "Withdrawn"},
        "color": "#C34242",
    },
    {
        "name": "Collection Ongoing",
        "statuses": {"Collection Ongoing"},
        "color": "#F0B840",
    },
    {
        "name": "Awaiting Response",
        "statuses": {"Waiting for Response"},
        "color": "#9e9e9e",
    },
    {
        "name": "Commission Responded",
        "statuses": {"Commission Engaged", "Rejected Legislation", "Law Passed"},
        "color": "#3CA371",
    },
]


def _eci_hover_list(titles: list[str]) -> str:
    if not titles:
        return "None"
    items = [f"• {t}" for t in titles[:MAX_HOVER_ITEMS]]
    result = "<br>".join(items)
    if len(titles) > MAX_HOVER_ITEMS:
        result += f"<br><i>… (and {len(titles) - MAX_HOVER_ITEMS} more)</i>"
    return result


def generate_chart_ecis_year(df: pd.DataFrame) -> str:
    years = sorted(df["registration_year"].dropna().unique())

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
            _eci_hover_list(
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
            text="ECI Outcomes by Registration Year",
            x=0.015,
            xanchor="left",
        ),
        xaxis=dict(title="Registration Year", tickmode="linear", dtick=1),
        yaxis=dict(title="Number of Initiatives"),
        barmode="stack",
        margin=MARGIN,
        height=HEIGHT,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    return wrap_card(fig.to_html(**DIV_ARGS))
