"""Renders a scrollable table of ECI initiatives that directly led to EU legislation."""

import pandas as pd

from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date
from page_creator.partials.lists.utils import build_card_title, generate_response_card

_STATUS = "Commission Engaged"
_HEADERS = ["Initiative", "Registration", "Objective", "Commission Response"]


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives with ``Commission Engaged`` status.

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


def generate_commission_engaged(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that led to passed legislation.

    Filters for rows with ``current_status == 'Law Passed'``, sorted by
    registration date descending.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``registration_date``, and
            ``legislation`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives law passed.
    """

    color = colors.commission_engaged
    df_sorted = _sort(_filter(df))
    title = build_card_title("🏛️", _STATUS, len(df_sorted), color)

    return generate_response_card(
        df_sorted,
        title,
        _HEADERS,
        color,
        empty_message="No initiatives have engaged the Commission yet.",
    )
