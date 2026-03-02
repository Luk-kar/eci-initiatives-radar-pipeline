import pandas as pd
import plotly.express as px

from page_creator.config import COLORS, MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card


def chart_policy_area(df: pd.DataFrame) -> str:
    agg = (
        df.groupby("primary_policy_area", as_index=False)["signatures_numeric"]
        .sum()
        .sort_values("signatures_numeric", ascending=False)
    )
    fig = px.bar(
        agg,
        x="primary_policy_area",
        y="signatures_numeric",
        color="primary_policy_area",
        color_discrete_sequence=COLORS,
        text_auto=".2s",
        title="Total Signatures by Policy Area",
        labels={
            "primary_policy_area": "Policy Area",
            "signatures_numeric": "Total Signatures",
        },
    )
    fig.update_layout(margin=MARGIN, height=HEIGHT, showlegend=True)
    return wrap_card(fig.to_html(**DIV_ARGS))
