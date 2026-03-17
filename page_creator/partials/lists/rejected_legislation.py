"""Renders a scrollable table of ECI initiatives that directly led to EU legislation."""

import pandas as pd

from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date
from page_creator.partials.lists.utils import build_card_title, generate_response_card

_STATUS = "Rejected Legislation"
_HEADERS = ["Initiative", "Registration", "Objective", "Response"]


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives with ``Rejected Legislation`` status.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_STATUS`` rows.
    """

    return df[df["current_status"] == _STATUS]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives with ``Rejected Legislation`` status.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_STATUS`` rows.
    """
    return sort_by_registration_date(df)


def generate_rejected_legislation(df: pd.DataFrame) -> str:
    """Filter for initiatives with ``Rejected Legislation`` status.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_STATUS`` rows.
    """

    color = colors.rejected_legislation
    df_sorted = _sort(_filter(df))
    title = build_card_title("❌", _STATUS, len(df_sorted), color)

    return generate_response_card(
        df_sorted,
        title,
        _HEADERS,
        color,
        empty_message="No initiatives have been rejected yet.",
    )
