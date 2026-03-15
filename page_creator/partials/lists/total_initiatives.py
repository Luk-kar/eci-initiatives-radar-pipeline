"""Renders a scrollable table of all registered ECI initiatives."""

import pandas as pd

from page_creator.partials.lists.utils import (
    build_initiative_row,
    normalise_registration_date,
    sig_cell,
    threshold_cell,
    wrap_table_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors

_HEADERS = [
    "Initiative",
    "Registration",
    "Objective",
    "Signatures",
    "Countries Threshold",
]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort all initiatives by registration date descending.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Full DataFrame sorted by ``registration_date`` descending.
    """
    return (
        normalise_registration_date(df)
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )


def _build_row(row: pd.Series) -> str:
    """Return a ``<tr>`` for a single initiative.

    Args:
        row: A DataFrame row. Must contain ``title``, ``url``, ``registration_date``,
             ``objective``, ``signatures_collected``, and ``signatures_threshold_met``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    extra = (
        f"\n          <td>{sig_cell(row['signatures_collected'])}</td>"
        f"\n          <td>{threshold_cell(row['signatures_threshold_met'])}</td>"
    )
    return build_initiative_row(row, extra)


def _build_rows(sorted_df: pd.DataFrame) -> str:
    """Iterate over all initiatives and concatenate their row HTML.

    Args:
        sorted_df: Sorted DataFrame of all initiatives.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(_build_row(row) for _, row in sorted_df.iterrows())


def generate_total_initiatives(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of all registered ECI initiatives.

    Sorted by registration date descending. Each row shows the initiative title
    (linked to its page), the registration date, a truncated objective, a signature
    progress bar towards the 1M target, and a country-threshold progress bar out of
    ``_COUNTRIES_THRESHOLD``.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``title``, ``url``,
            ``objective``, ``registration_date``, ``signatures_collected``, and
            ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div.
    """
    sorted_df = _sort(df)

    title = (
        '<h3 class="card__title">📋 Total Initiatives: '
        f'<span class="card__count" style="color:{colors.total_initiatives}">{len(sorted_df)}</span>'
        "</h3>"
    )

    return wrap_table_card(
        title, _build_rows(sorted_df), sorted_df, _HEADERS, colors.total_initiatives
    )
