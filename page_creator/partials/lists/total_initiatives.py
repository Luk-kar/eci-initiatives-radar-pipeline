"""Renders a scrollable table of all registered ECI initiatives."""

import pandas as pd

from page_creator.partials.lists.utils import (
    build_card_title,
    generate_sig_threshold_card,
    sort_by_registration_date,
)
from page_creator.partials.styles.colors import kpi_colors as colors


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort all initiatives by registration date descending.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Full DataFrame sorted by ``registration_date`` descending.
    """

    return sort_by_registration_date(df)


def generate_total_initiatives(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of all registered ECI initiatives.

    Sorted by registration date descending. Each row shows the initiative title
    (linked to its page), the registration date, a truncated objective, a signature
    progress bar towards the 1M target, and a country-threshold progress bar out of
    ``COUNTRIES_THRESHOLD``.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``title``, ``initiative_url``,
            ``objective``, ``registration_date``, ``signatures_collected``, and
            ``signatures_countries_threshold_met_count`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div.
    """

    color = colors.total_initiatives
    df_sorted = _sort(df)
    title = build_card_title("📋", "All Initiatives", len(df_sorted), color)

    return generate_sig_threshold_card(
        df_sorted,
        title,
        color,
        empty_message="No initiatives found.",
    )
