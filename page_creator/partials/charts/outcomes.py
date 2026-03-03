import pandas as pd
import plotly.express as px

from page_creator.config import MARGIN, HEIGHT, DIV_ARGS
from page_creator.utils import wrap_card


def generate_chart_outcomes(df: pd.DataFrame) -> str:
    counts = df["current_status"].value_counts().reset_index()
    counts.columns = ["current_status", "count"]
    fig = px.pie(
        counts,
        names="current_status",
        values="count",
        hole=0.45,
        title="Initiatives by Commission Outcome",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_traces(textinfo="percent+label", textposition="inside")
    fig.update_layout(margin=MARGIN, height=HEIGHT, showlegend=False)
    return wrap_card(fig.to_html(**DIV_ARGS), extra_class="bottom-col")
