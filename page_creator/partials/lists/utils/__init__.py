"""Shared HTML-generation helpers for list and table partials."""

from page_creator.partials.lists.utils.constants import (
    COUNTRIES_THRESHOLD,
    DEFAULT_TRUNCATE,
    SCROLL_THRESHOLD,
    SIG_TARGET,
)
from page_creator.partials.lists.utils.dates import normalise_registration_date
from page_creator.partials.lists.utils.progress import progress_bar
from page_creator.partials.lists.utils.rows import (
    HEADERS_WITH_SIGNATURES,
    build_initiative_row,
    build_sig_threshold_row,
    build_sig_threshold_rows,
    wrap_sig_threshold_card,
)
from page_creator.partials.lists.utils.signatures import sig_cell, threshold_cell
from page_creator.partials.lists.utils.table import build_table, wrap_table_card
from page_creator.partials.lists.utils.text import truncate

__all__ = [
    # constants
    "COUNTRIES_THRESHOLD",
    "DEFAULT_TRUNCATE",
    "SCROLL_THRESHOLD",
    "SIG_TARGET",
    # dates
    "normalise_registration_date",
    # progress
    "progress_bar",
    # rows
    "HEADERS_WITH_SIGNATURES",
    "build_initiative_row",
    "build_sig_threshold_row",
    "build_sig_threshold_rows",
    "wrap_sig_threshold_card",
    # signatures
    "sig_cell",
    "threshold_cell",
    # table
    "build_table",
    "wrap_table_card",
    # text
    "truncate",
]
