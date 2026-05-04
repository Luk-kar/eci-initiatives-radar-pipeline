"""Signature and countries-threshold cell builders for ECI initiative tables."""

import pandas as pd

from page_creator.partials.lists.utils.constants import (
    SIG_TARGET,
    COUNTRIES_THRESHOLD,
)
from page_creator.partials.lists.utils.progress import progress_bar


def sig_cell(value) -> str:
    """Return formatted signatures cell content with progress bar, or ``Collection not started``.

    Args:
        value: Raw ``signatures_collected`` value from a DataFrame row.

    Returns:
        An HTML string for the signatures table cell content (without ``<td>`` tags).
    """
    if pd.notna(value):
        sig_val = int(value)
        return f"{sig_val:,}{progress_bar(sig_val / SIG_TARGET * 100, 'signatures')}"
    return "Collection not started"


def threshold_cell(value) -> str:
    """
    Return formatted countries-threshold cell content with progress bar,
    or ``Collection not started``.

    Args:
        value: Raw ``signatures_countries_threshold_met_count`` value from a DataFrame row.

    Returns:
        An HTML string for the threshold table cell content (without ``<td>`` tags).
    """
    if pd.notna(value):
        thr_val = int(value)
        return (
            f"{thr_val} / {COUNTRIES_THRESHOLD}"
            f"{progress_bar(thr_val / COUNTRIES_THRESHOLD * 100, 'threshold')}"
        )
    return "Collection not started"
