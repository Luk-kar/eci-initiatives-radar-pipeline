"""Renders a scrollable table of ECI initiatives that reached the 1M signature threshold."""

import pandas as pd

from page_creator.partials.lists.utils import (
    build_card_title,
    generate_sig_threshold_card,
    SIG_TARGET,
)
from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that reached 1M signatures.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame where ``signatures_collected >= 1_000_000``.
    """
    return df[df["signatures_collected"] >= SIG_TARGET]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending.

    Args:
        df: Filtered DataFrame of initiatives that reached 1M signatures.

    Returns:
        Sorted and date-normalised DataFrame.
    """

    return sort_by_registration_date(df)


def generate_reached_signatures(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that reached 1M signatures.

    Filters for rows where ``signatures_collected >= 1_000_000``, sorted by
    registration date descending. Each row shows the initiative title (linked to
    its page), the registration date, a truncated objective, a signature progress
    bar, and a country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``signatures_collected``,
            ``title``, ``url``, ``objective``, ``registration_date``, and
            ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives reached the threshold.
    """

    color = colors.reached_signatures
    df_sorted = _sort(_filter(df))
    title = build_card_title("✅", "Reached 1M Signatures", len(df_sorted), color)

    return generate_sig_threshold_card(
        df_sorted,
        title,
        color,
        empty_message="No initiatives have reached 1M signatures.",
    )
