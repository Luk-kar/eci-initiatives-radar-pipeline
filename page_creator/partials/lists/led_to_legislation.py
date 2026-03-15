"""Renders a scrollable table of ECI initiatives that directly led to EU legislation."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    build_initiative_row,
    normalise_registration_date,
    truncate,
    wrap_table_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors

_STATUS = "Law Passed"
_HEADERS = ["Initiative", "Registration", "Objective", "Legislation Example"]


def _filter_and_sort(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives with ``Law Passed`` status, sorted by registration date.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered and sorted DataFrame containing only ``_STATUS`` rows.
    """
    return normalise_registration_date(
        df[df["current_status"] == _STATUS]
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )


def _build_row(row: pd.Series) -> str:
    """Return a ``<tr>`` for a single initiative that led to legislation.

    Args:
        row: A DataFrame row. Must contain ``title``, ``url``, ``registration_date``,
             ``objective``, and optionally ``legislation``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    # TODO: replace fallback once legislation column is added to the dataset
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
    registration date descending. The Legislation column uses a fallback
    placeholder until real legislative reference data is added to the dataset.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, and ``registration_date`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives led to legislation.
    """
    filtered_df = _filter_and_sort(df)

    title = (
        '<h3 class="card__title">⚖️ Led to Legislation: '
        "<span "
        f'class="card__count" style="color:{colors.led_to_legislation}">{len(filtered_df)}'
        "</span>"
        "</h3>"
    )

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have led to legislation yet.</p>'
        return wrap_card(title + body)

    return wrap_table_card(
        title,
        _build_rows(filtered_df),
        filtered_df,
        _HEADERS,
        colors.led_to_legislation,
    )
