"""Renders a scrollable table of ECI initiatives that received an EU Commission response."""

import pandas as pd

from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date
from page_creator.partials.lists.utils import build_card_title, generate_response_card

_RESPONSE_STATUSES = frozenset(
    ["Commission Engaged", "Law Passed", "Rejected Legislation"]
)
_HEADERS = ["Initiative", "Registration", "Objective", "Response"]


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that received a Commission response.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_RESPONSE_STATUSES`` rows.
    """

    return df[df["current_status"].isin(_RESPONSE_STATUSES)]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending.

    Args:
        df: Filtered DataFrame of initiatives with a Commission response.

    Returns:
        Sorted and date-normalised DataFrame.
    """
    return sort_by_registration_date(df)


def generate_got_response(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that received a Commission response.

    Filters for rows with ``current_status`` in ``_RESPONSE_STATUSES``, sorted by
    registration date descending. Each row shows the initiative title (linked to
    its page), the registration date, a truncated objective, and the truncated
    commission response text.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``registration_date``, and
            ``commission_answer_text`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives received a response.
    """

    color = colors.got_response
    df_sorted = _sort(_filter(df))
    title = build_card_title("📬", "Got EU Response", len(df_sorted), color)

    return generate_response_card(
        df_sorted,
        title,
        _HEADERS,
        color,
        empty_message="No initiatives have received an EU Commission response.",
    )
