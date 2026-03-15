"""Renders a scrollable table of ECI initiatives that reached the 1M signature threshold."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    normalise_registration_date,
    wrap_sig_threshold_card,
    SIG_TARGET,
)
from page_creator.partials.styles.colors import kpi_colors as colors


def _filter_and_sort(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that reached 1M signatures, sorted by registration date.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered and sorted DataFrame where ``signatures_collected >= 1_000_000``.
    """
    return normalise_registration_date(
        df[df["signatures_collected"] >= SIG_TARGET]
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )


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
    filtered_df = _filter_and_sort(df)

    title = (
        '<h3 class="card__title">'
        "✅ Reached 1M Signatures: "
        f'<span class="card__count" style="color:{colors.reached_signatures}">{len(filtered_df)}</span>'
        "</h3>"
    )

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have reached 1M signatures.</p>'
        return wrap_card(title + body)

    return wrap_sig_threshold_card(title, filtered_df, colors.reached_signatures)
