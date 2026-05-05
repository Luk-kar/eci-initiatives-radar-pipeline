"""Renders a scrollable table of ECI initiatives that directly led to EU legislation."""

import pandas as pd

from page_creator.partials.lists.utils import (
    build_card_title,
    build_initiative_row,
    normalise_registration_date,
    truncate,
    wrap_table_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date
from page_creator.utils import wrap_card

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
    """Return a ``<tr>`` for a single initiative that law passed.

    Args:
        row: A DataFrame row. Must contain ``title``, ``initiative_url``, ``registration_date``,
             ``objective``, and ``legislation``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    raw = row["law_passed"]
    legislation = truncate(raw) if pd.notna(raw) and raw else "—"
    return build_initiative_row(row, f"\n          <td>{legislation}</td>")


def _build_rows(filtered_df: pd.DataFrame) -> str:
    """Iterate over all matching initiatives and concatenate their row HTML.

    Args:
        filtered_df: Filtered and sorted DataFrame.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(_build_row(row) for _, row in filtered_df.iterrows())


def generate_law_passed(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that led to passed legislation.

    Filters for rows with ``current_status == 'Law Passed'``, sorted by
    registration date descending.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``initiative_url``, ``objective``, ``registration_date``, and
            ``legislation`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives law passed.
    """

    df_filtered = _filter(df)
    df_sorted = _sort(df_filtered)
    df_final = normalise_registration_date(df_sorted)

    color = colors.law_passed
    title = build_card_title("⚖️", "Law Passed", len(df_final), color)

    if df_final.empty:

        return wrap_card(
            title + '<p class="list-empty">No initiatives have law passed yet.</p>'
        )

    return wrap_table_card(title, _build_rows(df_final), df_final, _HEADERS, color)
