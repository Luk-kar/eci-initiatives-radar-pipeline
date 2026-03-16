"""Renders a scrollable table of all registered ECI initiatives."""

import pandas as pd

from page_creator.partials.lists.utils import (
    normalise_registration_date,
    wrap_sig_threshold_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort all initiatives by registration date descending.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Full DataFrame sorted by ``registration_date`` descending.
    """
    df = df.copy()

    df["registration_date"] = pd.to_datetime(
        df["registration_date"], dayfirst=True
    ).dt.date  # ← keep as datetime.date, not string

    return df.sort_values("registration_date", ascending=False).reset_index(drop=True)


def generate_total_initiatives(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of all registered ECI initiatives.

    Sorted by registration date descending. Each row shows the initiative title
    (linked to its page), the registration date, a truncated objective, a signature
    progress bar towards the 1M target, and a country-threshold progress bar out of
    ``COUNTRIES_THRESHOLD``.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``title``, ``url``,
            ``objective``, ``registration_date``, ``signatures_collected``, and
            ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div.
    """
    sorted_df = _sort(df)

    title = (
        '<h3 class="card__title">📋 Total Initiatives: '
        "<span "
        f'class="card__count" style="color:{colors.total_initiatives}">{len(sorted_df)}'
        "</span>"
        "</h3>"
    )

    return wrap_sig_threshold_card(title, sorted_df, colors.total_initiatives)
