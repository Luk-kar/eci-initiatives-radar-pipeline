import pandas as pd
import plotly.express as px

from page_creator.config import COLORS, MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card


def generate_chart_signatures_year(df: pd.DataFrame) -> str:
    fig = px.scatter(
        df,
        x="registration_year",
        y="signatures_collected",
        size="signatures_collected",
        hover_name="title",
        color_discrete_sequence=COLORS,
        title="Signatures per Initiative by Year",
        labels={
            "registration_year": "Registration Year",
            "signatures_collected": "Total Signatures",
        },
        size_max=60,
    )
    fig.update_layout(
        margin=MARGIN,
        height=HEIGHT,
        xaxis=dict(dtick=1),
        legend=dict(title_text="primary_policy_area", itemsizing="constant"),
    )
    return wrap_card(fig.to_html(**DIV_ARGS), extra_class="bottom-col")
