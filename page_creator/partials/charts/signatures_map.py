"""Renders a choropleth map of total ECI signatures collected per EU member state."""

# ─── Standard Library ────────────────────────────────────────────────────────
import ast

# ─── Third-Party ─────────────────────────────────────────────────────────────
import pandas as pd
import plotly.graph_objects as go

# ─── Local ───────────────────────────────────────────────────────────────────
from page_creator.config import DIV_ARGS
from page_creator.utils import wrap_card
from page_creator.partials.styles.colors import kpi_colors

# ─── Map Display Constants ───────────────────────────────────────────────────

MAP_HEIGHT = 500
MAP_WIDTH = 1000

# Maximum number of top ECIs shown per country in the hover tooltip.
MAX_HOVER_ITEMS = 10

# Extra horizontal padding (degrees) added to the Europe longitude clip range.
_EUROPE_LONGITUDE_PADDING = 16


# ─── Country Registry ────────────────────────────────────────────────────────
# Maps alpha-2 code → (display name, alpha-3, latitude, longitude).
# Latitude/longitude values are approximate country centroids used for label
# placement on the map.

_COUNTRIES: dict[str, tuple[str, str, float, float]] = {
    "AT": ("Austria", "AUT", 47.5, 14.5),
    "BE": ("Belgium", "BEL", 50.6, 4.6),
    "BG": ("Bulgaria", "BGR", 42.7, 25.5),
    "CY": ("Cyprus", "CYP", 35.0, 33.0),
    "CZ": ("Czechia", "CZE", 49.8, 15.5),
    "DE": ("Germany", "DEU", 51.0, 10.5),
    "DK": ("Denmark", "DNK", 56.0, 10.0),
    "EE": ("Estonia", "EST", 59.0, 26.0),
    "ES": ("Spain", "ESP", 40.0, -4.0),
    "FI": ("Finland", "FIN", 64.0, 26.0),
    "FR": ("France", "FRA", 46.6, 2.3),
    "GR": ("Greece", "GRC", 39.0, 22.0),
    "HR": ("Croatia", "HRV", 45.5, 16.0),
    "HU": ("Hungary", "HUN", 47.0, 19.5),
    "IE": ("Ireland", "IRL", 53.0, -8.0),
    "IT": ("Italy", "ITA", 42.8, 12.8),
    "LT": ("Lithuania", "LTU", 55.3, 23.9),
    "LU": ("Luxembourg", "LUX", 49.8, 6.1),
    "LV": ("Latvia", "LVA", 57.0, 25.0),
    "MT": ("Malta", "MLT", 35.9, 14.4),
    "NL": ("Netherlands", "NLD", 52.3, 5.3),
    "PL": ("Poland", "POL", 52.0, 19.0),
    "PT": ("Portugal", "PRT", 39.5, -8.0),
    "RO": ("Romania", "ROU", 46.0, 25.0),
    "SE": ("Sweden", "SWE", 62.0, 15.0),
    "SI": ("Slovenia", "SVN", 46.1, 15.0),
    "SK": ("Slovakia", "SVK", 48.7, 19.5),
}

# Reverse lookup: display name → alpha-2 (e.g. "Germany" → "DE").
# Built once from _COUNTRIES so country-keyed rows using full names are resolved.
_NAME_TO_ALPHA2: dict[str, str] = {name: a2 for a2, (name, *_) in _COUNTRIES.items()}


# ─── Country-Keyed Output Schema ─────────────────────────────────────────────
# Column order for the aggregated country DataFrame produced by _build_country_df.

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


# ─── Label Outline Offsets ───────────────────────────────────────────────────
# Eight (dx, dy) pairs used to draw a dark stroke around map labels by rendering
# slightly shifted copies before the white text layer.

_LABEL_OFFSETS: list[tuple[float, float]] = [
    (-0.15, 0.00),
    (0.15, 0.00),
    (0.00, -0.15),
    (0.00, 0.15),
    (-0.10, -0.10),
    (-0.10, 0.10),
    (0.10, -0.10),
    (0.10, 0.10),
]


# ─── Plotly Config ───────────────────────────────────────────────────────────
# Passed to fig.to_html(); disables zoom/pan controls for an embedded read-only map.

_MAP_CONFIG = {
    "responsive": True,
    "scrollZoom": False,
    "displayModeBar": False,
}


# ─── Formatting Helpers ──────────────────────────────────────────────────────


def _format_sigs(n: int) -> str:
    """Return a compact human-readable string for a signature count.

    Examples:
        1_200_000 → '1.2M'
        45_000    → '45K'
        750       → '750'
    """
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


# ─── Parsing Helpers ─────────────────────────────────────────────────────────


def _parse_count(raw_value: str | int | dict) -> int:
    """Extract a plain integer from a raw per-country value.

    Handles two input shapes:
      - Legacy int/str format: ``57643`` or ``"57,643"``
      - New nested-dict format: ``{'signatures': 57643, 'threshold': ..., 'percentage': ...}``
    """
    raw = raw_value.get("signatures", 0) if isinstance(raw_value, dict) else raw_value
    return int(str(raw).replace(",", "").replace("*", ""))


def _resolve_alpha2(key: str) -> str | None:
    """Resolve a country key to a known alpha-2 code, or return None if unrecognised.

    Accepts both alpha-2 codes (``"DE"``) and full display names (``"Germany"``).
    """
    return key if key in _COUNTRIES else _NAME_TO_ALPHA2.get(key)


def _parse_breakdown(raw: str) -> dict:
    """Parse the ``signatures_collected_by_country`` cell into a plain dict.

    Returns an empty dict when the value is missing, NaN, or an empty string.
    """
    return ast.literal_eval(raw) if raw and not pd.isna(raw) else {}


# ─── Per-Row Aggregation ─────────────────────────────────────────────────────


def _accumulate_row(
    breakdown: dict,
    title: str,
    totals: dict[str, int],
    threshold_met: dict[str, int],
    top_ecis: dict[str, list[tuple[int, str]]],
) -> None:
    """Fold one ECI initiative's country breakdown into the running aggregation dicts.

    Args:
        breakdown:     Per-country signature data for a single ECI row.
        title:         Initiative title used to label entries in ``top_ecis``.
        totals:        Running total signatures per alpha-2 country code.
        threshold_met: Running count of initiatives that met the national threshold
                       per alpha-2 country code (new-format rows only).
        top_ecis:      Running list of ``(count, title)`` pairs per alpha-2 code.
    """
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


# ─── Country DataFrame Assembly ──────────────────────────────────────────────


def _build_country_row(
    alpha2: str,
    total: int,
    threshold_met: dict[str, int],
    top_ecis: dict[str, list[tuple[int, str]]],
) -> dict:
    """
    Build a single row dict for the aggregated country DataFrame.

    The ``eci_list`` field is an HTML-formatted ranked list of top initiatives
    for use inside the Plotly hover tooltip.
    """

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


def _build_country_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate per-country signature totals across all ECI initiatives.

    Iterates the raw DataFrame, parses each row's ``signatures_collected_by_country``
    column, and accumulates totals, threshold-met counts, and a ranked ECI list
    per country.

    Returns:
        A DataFrame with columns defined by ``_COUNTRY_DF_COLUMNS``, sorted
        descending by total signatures. Returns an empty DataFrame with the
        same schema when no country-level data is present.
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
        _build_country_row(a2, total, threshold_met, top_ecis)
        for a2, total in totals.items()
    ]

    return (
        pd.DataFrame(rows).sort_values("total", ascending=False).reset_index(drop=True)
    )


# ─── Plotly Trace Builders ───────────────────────────────────────────────────


def _build_choropleth_trace(cdf: pd.DataFrame) -> go.Choropleth:
    """Return the Viridis-scaled choropleth fill layer with hover tooltip."""

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


def _build_label_outline_traces(cdf: pd.DataFrame) -> list[go.Scattergeo]:
    """
    Return 8 dark-outline Scattergeo layers that make country labels legible.

    Each layer is offset by one of the ``_LABEL_OFFSETS`` vectors to simulate
    a text stroke effect, since Plotly has no native text-outline support.
    """

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
    """Return the white text layer rendered on top of the outline traces."""

    return go.Scattergeo(
        lon=cdf["lon"],
        lat=cdf["lat"],
        text=cdf["label"],
        mode="text",
        textfont=dict(size=10, color="white", family="Arial Black"),
        hoverinfo="skip",
        showlegend=False,
    )


# ─── Figure Layout ───────────────────────────────────────────────────────────


def _apply_geo_layout(fig: go.Figure, total_sigs: str) -> None:
    """Configure geo projection, Europe clip bounds, title, and figure dimensions.

    Mutates ``fig`` in place.

    Args:
        fig:        The Plotly figure to update.
        total_sigs: Pre-formatted total signature count used in the chart title.
    """

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


# ─── Public API ──────────────────────────────────────────────────────────────


def generate_chart_signatures_map(df: pd.DataFrame) -> str:
    """
    Return an HTML card containing a choropleth map of ECI signatures by EU member state.

    Renders a Viridis-scaled choropleth fill countries layer with white signature-count
    labels (outlined in dark purple for legibility) positioned at each country's
    centroid. The map is clipped to Europe and has zoom and toolbar controls
    disabled. Each country's hover tooltip shows total signatures, how many ECIs
    met the national threshold, and a ranked list of top contributing initiatives.

    Args:
        df: The full ECI initiatives DataFrame. Must contain:

            - ``signatures_collected_by_country``:

                Python dict literal (as a string)
                representing per-country breakdowns, parsed via ``ast.literal_eval``.
                Keyed by country name or alpha-2 code; values are either a plain
                integer (legacy format) or a nested dict with ``signatures``,
                ``threshold``, and ``percentage`` keys (new format).

              - ``title``:

                Human-readable initiative title.

    Returns:
        An HTML string wrapping the Plotly map in a ``card`` div, or a card
        containing a fallback message if no country-level data is available.
    """

    country_signatures_df = _build_country_df(df)

    if country_signatures_df.empty:
        raise ValueError(
            "No country-level signature data found. "
            "The 'signatures_collected_by_country' column contains no parseable "
            "per-country breakdowns for any row in the provided DataFrame."
        )

    fig = go.Figure()
    fig.add_trace(_build_choropleth_trace(country_signatures_df))

    for trace in _build_label_outline_traces(country_signatures_df):
        fig.add_trace(trace)

    fig.add_trace(_build_label_trace(country_signatures_df))

    _apply_geo_layout(fig, _format_sigs(int(country_signatures_df["total"].sum())))

    return wrap_card(fig.to_html(**{**DIV_ARGS, "config": _MAP_CONFIG}))
