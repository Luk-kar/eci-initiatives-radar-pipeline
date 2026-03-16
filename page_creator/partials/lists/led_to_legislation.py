"""Renders a scrollable table of ECI initiatives that directly led to EU legislation."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    normalise_registration_date,
    build_initiative_row,
    truncate,
    wrap_table_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date

_STATUS = "Law Passed"
_HEADERS = ["Initiative", "Registration", "Objective", "Legislation Example"]


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives with ``Law Passed`` status.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_STATUS`` rows.
    """
    return df[df["current_status"] == _STATUS]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending.

    Args:
        df: Filtered DataFrame of ``Law Passed`` initiatives.

    Returns:
        Sorted and date-normalised DataFrame.
    """

    return sort_by_registration_date(df)


def _build_row(row: pd.Series) -> str:
    """Return a ``<tr>`` for a single initiative that led to legislation.

    Args:
        row: A DataFrame row. Must contain ``title``, ``url``, ``registration_date``,
             ``objective``, and ``legislation``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    legislation = truncate(row["legislation"])
    return build_initiative_row(row, f"\n          <td>{legislation}</td>")


def _build_rows(filtered_df: pd.DataFrame) -> str:
    """Iterate over all matching initiatives and concatenate their row HTML.

    Args:
        filtered_df: Filtered and sorted DataFrame.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(_build_row(row) for _, row in filtered_df.iterrows())


def generate_led_to_legislation(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that led to passed legislation.

    Filters for rows with ``current_status == 'Law Passed'``, sorted by
    registration date descending.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``registration_date``, and
            ``legislation`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives led to legislation.
    """
    df_filtered = _filter(df)
    df_sorted = _sort(df_filtered)
    df_final = normalise_registration_date(df_sorted)

    title = (
        '<h3 class="card__title">⚖️ Led to Legislation: '
        "<span "
        f'class="card__count" style="color:{colors.led_to_legislation}">{len(df_final)}'
        "</span>"
        "</h3>"
    )

    if df_final.empty:
        body = '<p class="list-empty">No initiatives have led to legislation yet.</p>'
        return wrap_card(title + body)

    return wrap_table_card(
        title,
        _build_rows(df_final),
        df_final,
        _HEADERS,
        colors.led_to_legislation,
    )
