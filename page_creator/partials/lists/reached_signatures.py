"""Renders a scrollable table of ECI initiatives that reached the 1M signature threshold."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    normalise_registration_date,
    wrap_sig_threshold_card,
    SIG_TARGET,
)
from page_creator.partials.styles.colors import kpi_colors as colors


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

    df = df.copy()

    df["registration_date"] = pd.to_datetime(
        df["registration_date"], dayfirst=True
    ).dt.date  # ← keep as datetime.date, not string

    return df.sort_values("registration_date", ascending=False).reset_index(drop=True)


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
    df_filtered = _filter(df)
    df_sorted = _sort(df_filtered)

    title = (
        '<h3 class="card__title">'
        "✅ Reached 1M Signatures: "
        "<span "
        f'class="card__count" style="color:{colors.reached_signatures}">{len(df_sorted)}'
        "</span>"
        "</h3>"
    )

    if df_sorted.empty:
        body = '<p class="list-empty">No initiatives have reached 1M signatures.</p>'
        return wrap_card(title + body)

    return wrap_sig_threshold_card(title, df_sorted, colors.reached_signatures)
