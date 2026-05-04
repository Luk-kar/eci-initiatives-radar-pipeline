"""Renders a scrollable table of ECI initiatives no longer in active collection."""

import pandas as pd

from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date
from page_creator.partials.lists.utils import (
    build_card_title,
    generate_sig_threshold_card,
)

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
            ``title``, ``initiative_url``, ``objective``, ``registration_date``,
            ``signatures_collected``, and ``signatures_countries_threshold_met_count`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives match.
    """

    color = colors.withdrawn
    df_sorted = _sort(_filter(df))
    title = build_card_title("🔙", _STATUS, len(df_sorted), color)

    return generate_sig_threshold_card(
        df_sorted,
        title,
        color,
        empty_message="No closed-collection initiatives found.",
    )
