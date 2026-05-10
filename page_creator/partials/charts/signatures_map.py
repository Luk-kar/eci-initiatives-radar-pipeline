"""Renders a choropleth map of total ECI signatures collected per EU member state."""

# Python
import ast
import json

# Third Party
import pandas as pd
import plotly.graph_objects as go

# Local
from page_creator.config import DIV_ARGS
from page_creator.utils import wrap_card
from page_creator.partials.styles.colors import kpi_colors

MAP_HEIGHT = 500
MAP_WIDTH = 1000
MAX_HOVER_ITEMS = 10

# Alpha-2 → (display name, alpha-3, latitude, longitude)
_COUNTRIES: dict[str, tuple[str, str, float, float]] = {
    "DE": ("Germany", "DEU", 51.0, 10.5),
    "FR": ("France", "FRA", 46.6, 2.3),
    "IT": ("Italy", "ITA", 42.8, 12.8),
    "ES": ("Spain", "ESP", 40.0, -4.0),
    "PL": ("Poland", "POL", 52.0, 19.0),
    "RO": ("Romania", "ROU", 46.0, 25.0),
    "NL": ("Netherlands", "NLD", 52.3, 5.3),
    "BE": ("Belgium", "BEL", 50.6, 4.6),
    "GR": ("Greece", "GRC", 39.0, 22.0),
    "CZ": ("Czechia", "CZE", 49.8, 15.5),
    "PT": ("Portugal", "PRT", 39.5, -8.0),
    "SE": ("Sweden", "SWE", 62.0, 15.0),
    "HU": ("Hungary", "HUN", 47.0, 19.5),
    "AT": ("Austria", "AUT", 47.5, 14.5),
    "BG": ("Bulgaria", "BGR", 42.7, 25.5),
    "DK": ("Denmark", "DNK", 56.0, 10.0),
    "SK": ("Slovakia", "SVK", 48.7, 19.5),
    "FI": ("Finland", "FIN", 64.0, 26.0),
    "IE": ("Ireland", "IRL", 53.0, -8.0),
    "HR": ("Croatia", "HRV", 45.5, 16.0),
    "LT": ("Lithuania", "LTU", 55.3, 23.9),
    "SI": ("Slovenia", "SVN", 46.1, 15.0),
    "LV": ("Latvia", "LVA", 57.0, 25.0),
    "EE": ("Estonia", "EST", 59.0, 26.0),
    "CY": ("Cyprus", "CYP", 35.0, 33.0),
    "LU": ("Luxembourg", "LUX", 49.8, 6.1),
    "MT": ("Malta", "MLT", 35.9, 14.4),
}


def _format_sigs(n: int) -> str:
    """Format a raw signature count into a compact human-readable string (e.g. 1200000 → '1.2M')."""

    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


# Reverse lookup: country display name → alpha-2
_NAME_TO_ALPHA2: dict[str, str] = {v[0]: k for k, v in _COUNTRIES.items()}


def _parse_count(raw_value: str | int | dict) -> int:
    """Extract integer from both old format (int) and new format (nested dict)."""

    raw = raw_value.get("signatures", 0) if isinstance(raw_value, dict) else raw_value
    return int(str(raw).replace(",", "").replace("*", ""))


def _resolve_alpha2(key: str) -> str | None:
    """Resolve a country key (alpha-2 or display name) to a known alpha-2 code."""

    return key if key in _COUNTRIES else _NAME_TO_ALPHA2.get(key)


def _parse_breakdown(raw: str) -> dict:
    """Safely parse a raw signatures_collected_by_country string into a dict."""

    return ast.literal_eval(raw) if raw and not pd.isna(raw) else {}


def _accumulate_row(
    breakdown: dict,
    title: str,
    totals: dict[str, int],
    threshold_met: dict[str, int],
    top_ecis: dict[str, list[tuple[int, str]]],
) -> None:
    """Accumulate one ECI row's breakdown into the running aggregation dicts."""

    for key, value in breakdown.items():

        alpha2 = _resolve_alpha2(key)

        if alpha2 is None:
            continue

        count = _parse_count(value)
        totals[alpha2] = totals.get(alpha2, 0) + count
        top_ecis.setdefault(alpha2, []).append((count, title))

        if isinstance(value, dict):
            try:
                if float(value.get("percentage", 0)) >= 100.0:
                    threshold_met[alpha2] = threshold_met.get(alpha2, 0) + 1
            except ValueError:
                pass


def _build_country_row(
    alpha2: str,
    total: int,
    threshold_met: dict[str, int],
    top_ecis: dict[str, list[tuple[int, str]]],
) -> dict:
    """Build a single output row dict for one country."""

    name, alpha3, lat, lon = _COUNTRIES[alpha2]

    ecis_sorted = sorted(top_ecis[alpha2], reverse=True)

    items = [f"• {t}: {_format_sigs(c)}" for c, t in ecis_sorted[:MAX_HOVER_ITEMS]]

    if len(ecis_sorted) > MAX_HOVER_ITEMS:
        items.append(f"<i>… (and {len(ecis_sorted) - MAX_HOVER_ITEMS} more)</i>")

    return {
        "alpha2": alpha2,
        "alpha3": alpha3,
        "name": name,
        "lat": lat,
        "lon": lon,
        "total": total,
        "threshold_met_count": threshold_met.get(alpha2, 0),
        "label": _format_sigs(total),
        "eci_list": "<br>".join(items),
    }


_COUNTRY_DF_COLUMNS = [
    "alpha2",
    "alpha3",
    "name",
    "lat",
    "lon",
    "total",
    "threshold_met_count",
    "label",
    "eci_list",
]


def _build_country_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate per-country signature totals,
    threshold-met counts, and
    top ECI lists from the raw JSON breakdown column.
    """
    totals: dict[str, int] = {}
    threshold_met: dict[str, int] = {}
    top_ecis: dict[str, list[tuple[int, str]]] = {}

    for _, row in df.iterrows():

        breakdown = _parse_breakdown(row["signatures_collected_by_country"])

        if breakdown:
            _accumulate_row(breakdown, row["title"], totals, threshold_met, top_ecis)

    if not totals:
        return pd.DataFrame(columns=_COUNTRY_DF_COLUMNS)

    rows = [
        _build_country_row(a2, t, threshold_met, top_ecis) for a2, t in totals.items()
    ]

    return (
        pd.DataFrame(rows).sort_values("total", ascending=False).reset_index(drop=True)
    )


def _build_choropleth_trace(cdf: pd.DataFrame) -> go.Choropleth:
    """Choropleth fill layer: Viridis-scaled countries with hover tooltip."""
    return go.Choropleth(
        locations=cdf["alpha3"],
        z=cdf["total"],
        text=cdf["name"],
        customdata=cdf[["total", "threshold_met_count", "eci_list"]].values,
        colorscale="Viridis",
        colorbar=dict(title="Total<br>Signatures", tickformat=","),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Total Signatures: %{customdata[0]:,.0f}<br>"
            "Signatures Threshold Met: %{customdata[1]:,.0f}<br><br>"
            "<b>Top ECIs:</b><br>%{customdata[2]}"
            "<extra></extra>"
        ),
        showscale=True,
    )


_LABEL_OFFSETS = [
    (-0.15, 0),
    (0.15, 0),
    (0, -0.15),
    (0, 0.15),
    (-0.1, -0.1),
    (-0.1, 0.1),
    (0.1, -0.1),
    (0.1, 0.1),
]


def _build_label_outline_traces(cdf: pd.DataFrame) -> list[go.Scattergeo]:
    """Dark-outline Scattergeo layers offset in 8 directions for label legibility."""
    return [
        go.Scattergeo(
            lon=cdf["lon"] + dx,
            lat=cdf["lat"] + dy,
            text=cdf["label"],
            mode="text",
            textfont=dict(
                size=10, color=kpi_colors.map_text_outline, family="Arial Black"
            ),
            hoverinfo="skip",
            showlegend=False,
        )
        for dx, dy in _LABEL_OFFSETS
    ]


def _build_label_trace(cdf: pd.DataFrame) -> go.Scattergeo:
    """White text layer rendered on top of the outline layers."""
    return go.Scattergeo(
        lon=cdf["lon"],
        lat=cdf["lat"],
        text=cdf["label"],
        mode="text",
        textfont=dict(size=10, color="white", family="Arial Black"),
        hoverinfo="skip",
        showlegend=False,
    )


_EUROPE_LONGITUDE_PADDING = 16


def _apply_geo_layout(fig: go.Figure, total_sigs: str) -> None:
    """Configure map projection, Europe clip bounds, title, and dimensions in-place."""
    fig.update_geos(
        scope="world",
        projection_type="natural earth",
        showland=True,
        landcolor="rgb(243, 243, 243)",
        coastlinecolor="rgb(204, 204, 204)",
        showcountries=True,
        countrycolor="rgb(204, 204, 204)",
        lataxis_range=[32, 72],
        lonaxis_range=[
            -14 - _EUROPE_LONGITUDE_PADDING,
            36 + _EUROPE_LONGITUDE_PADDING,
        ],
    )
    fig.update_layout(
        title=dict(
            text=f"ECI Signatures by Country ({total_sigs} total)",
            x=0.015,
            xanchor="left",
        ),
        height=MAP_HEIGHT,
        width=MAP_WIDTH,
        margin=dict(l=0, r=0, t=50, b=0),
        dragmode=False,
    )


_MAP_CONFIG = {
    "responsive": True,
    "scrollZoom": False,
    "displayModeBar": False,
}


def generate_chart_signatures_map(df: pd.DataFrame) -> str:
    """
    Return an HTML card containing a choropleth map of ECI signatures by EU member state.

    Renders a Viridis-scaled choropleth fill layer with white signature-count
    labels (outlined in dark purple for legibility) positioned at each country's
    centroid. The map is clipped to Europe and has zoom and toolbar controls
    disabled. Each country's hover tooltip shows total signatures, how many ECIs
    met the national threshold, and a ranked list of top contributing initiatives.

    Args:
        df: The full ECI initiatives DataFrame. Must contain a
            ``signatures_collected_by_country`` column with JSON-encoded
            per-country breakdowns and a ``title`` column.

    Returns:
        An HTML string wrapping the Plotly map in a ``card`` div, or a card
        containing a fallback message if no country-level data is available.
    """

    cdf = _build_country_df(df)

    if cdf.empty:
        return wrap_card("<p>No country-level signature data available.</p>")

    fig = go.Figure()

    fig.add_trace(_build_choropleth_trace(cdf))

    for trace in _build_label_outline_traces(cdf):
        fig.add_trace(trace)

    fig.add_trace(_build_label_trace(cdf))

    _apply_geo_layout(fig, _format_sigs(int(cdf["total"].sum())))

    return wrap_card(fig.to_html(**{**DIV_ARGS, "config": _MAP_CONFIG}))
