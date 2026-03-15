"""Renders a scrollable table of ECI initiatives that reached the 1M signature threshold."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    build_initiative_row,
    normalise_registration_date,
    progress_bar,
    wrap_table_card,
    _SIG_TARGET,
    _COUNTRIES_THRESHOLD,
)
from page_creator.partials.styles.colors import kpi_colors as colors

_HEADERS = [
    "Initiative",
    "Registration",
    "Objective",
    "Signatures",
    "Countries Threshold",
]


def _filter_and_sort(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that reached 1M signatures, sorted by registration date.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered and sorted DataFrame where ``signatures_collected >= 1_000_000``.
    """
    return normalise_registration_date(
        df[df["signatures_collected"] >= _SIG_TARGET]
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )


def _sig_cell(value) -> str:
    """Return a formatted signatures cell content with progress bar.

    Unlike ``currently_open``, this filter guarantees ``signatures_collected``
    is always >= 1M, so no ``N/A`` fallback is needed here.

    Args:
        value: Raw ``signatures_collected`` value from the DataFrame row.

    Returns:
        An HTML string for the signatures table cell content (without ``<td>`` tags).
    """
    sig_val = int(value)
    return f"{sig_val:,}{progress_bar(sig_val / _SIG_TARGET * 100, 'signatures')}"


def _threshold_cell(value) -> str:
    """Return a formatted countries-threshold cell content with progress bar, or ``N/A``.

    Args:
        value: Raw ``signatures_threshold_met`` value from the DataFrame row.

    Returns:
        An HTML string for the threshold table cell content (without ``<td>`` tags).
    """
    if pd.notna(value):
        thr_val = int(value)
        return (
            f"{thr_val} / {_COUNTRIES_THRESHOLD}"
            f"{progress_bar(thr_val / _COUNTRIES_THRESHOLD * 100, 'threshold')}"
        )
    return "N/A"


def _build_row(row: pd.Series) -> str:
    """Return a ``<tr>`` for a single initiative that reached 1M signatures.

    Args:
        row: A DataFrame row. Must contain ``title``, ``url``, ``registration_date``,
             ``objective``, ``signatures_collected``, and ``signatures_threshold_met``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    extra = (
        f"\n          <td>{_sig_cell(row['signatures_collected'])}</td>"
        f"\n          <td>{_threshold_cell(row['signatures_threshold_met'])}</td>"
    )
    return build_initiative_row(row, extra)


def _build_rows(filtered_df: pd.DataFrame) -> str:
    """Iterate over all matching initiatives and concatenate their row HTML.

    Args:
        filtered_df: Filtered and sorted DataFrame.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(_build_row(row) for _, row in filtered_df.iterrows())


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

    return wrap_table_card(
        title,
        _build_rows(filtered_df),
        filtered_df,
        _HEADERS,
        colors.reached_signatures,
    )
