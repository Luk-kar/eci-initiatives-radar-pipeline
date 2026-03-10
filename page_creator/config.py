"""Shared Plotly layout constants used across all chart generators."""

import plotly.express as px

COLORS = px.colors.qualitative.Plotly
MARGIN = {"l": 20, "r": 20, "t": 50, "b": 20}
HEIGHT = 400
DIV_ARGS = {
    "full_html": False,
    "include_plotlyjs": False,
    "config": {"responsive": True},
}
