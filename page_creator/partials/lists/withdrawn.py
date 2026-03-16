"""Renders a scrollable table of ECI initiatives no longer in active collection."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    normalise_registration_date,
    wrap_sig_threshold_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date

_STATUS = "Withdrawn"


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that are no longer in active collection.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_STATUS`` rows.
    """
    return df[df["current_status"] == _STATUS]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending.

    Args:
        df: Filtered DataFrame of closed-collection initiatives.

    Returns:
        Sorted and date-normalised DataFrame.
    """
    return sort_by_registration_date(df)


def generate_withdrawn(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs no longer in active collection.

    Filters for rows with ``current_status`` in ``_STATUSES``, sorted by
    registration date descending. Each row shows the initiative title (linked to
    its page), the registration date, a truncated objective, a signature progress
    bar, and a country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``registration_date``,
            ``signatures_collected``, and ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives match.
    """
    df_filtered = _filter(df)
    df_sorted = _sort(df_filtered)
    df_final = normalise_registration_date(df_sorted)

    title = (
        '<h3 class="card__title">'
        f"🔙 {_STATUS}: "
        f'<span class="card__count" style="color:{colors.withdrawn}">{len(df_final)}</span>'
        "</h3>"
    )

    if df_final.empty:
        body = '<p class="list-empty">No closed-collection initiatives found.</p>'
        return wrap_card(title + body)

    return wrap_sig_threshold_card(title, df_final, colors.withdrawn)
