"""Shared HTML row and cell builders for ECI initiative tables."""

import pandas as pd

from page_creator.partials.lists.utils.signatures import sig_cell, threshold_cell
from page_creator.partials.lists.utils.table import build_table, wrap_table_card
from page_creator.partials.lists.utils.text import truncate


# Shared column headers for tables that include signature and threshold columns
HEADERS_WITH_SIGNATURES = [
    "Initiative",
    "Registration",
    "Objective",
    "Signatures",
    "Countries Threshold",
]


def build_initiative_row(row: pd.Series, extra_cells: str = "") -> str:
    """Return a ``<tr>`` with the common Initiative / Registration / Objective cells.

    Args:
        row:         A DataFrame row. Must contain ``title``, ``url``,
                     ``registration_date``, and ``objective``.
        extra_cells: Additional ``<td>`` HTML appended after the three base cells.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    url = row.get("url") or "#"
    registration = row["registration_date"]
    objective = truncate(row.get("objective", ""))
    return f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{registration}</td>
          <td>{objective}</td>{extra_cells}
        </tr>"""


def build_sig_threshold_row(row: pd.Series) -> str:
    """Return a ``<tr>`` with Initiative / Registration / Objective / Signatures / Threshold cells.

    Shared by ``reached_signatures`` and ``total_initiatives`` which have identical
    row structure. Eliminates the duplicated ``_build_row`` in both modules.

    Args:
        row: A DataFrame row. Must contain ``title``, ``url``, ``registration_date``,
             ``objective``, ``signatures_collected``, and ``signatures_threshold_met``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    extra = (
        f"\n          <td>{sig_cell(row['signatures_collected'])}</td>"
        f"\n          <td>{threshold_cell(row['signatures_threshold_met'])}</td>"
    )
    return build_initiative_row(row, extra)


def build_sig_threshold_rows(df: pd.DataFrame) -> str:
    """Iterate over a DataFrame and concatenate ``<tr>`` HTML for each row.

    Shared by ``reached_signatures`` and ``total_initiatives``.

    Args:
        df: DataFrame of initiatives. Each row is passed to ``build_sig_threshold_row``.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(build_sig_threshold_row(row) for _, row in df.iterrows())


def wrap_sig_threshold_card(
    title: str,
    df: pd.DataFrame,
    scrollbar_color: str,
) -> str:
    """Render a complete signatures+threshold card from a filtered DataFrame.

    Combines ``build_sig_threshold_rows`` and ``wrap_table_card`` into a single
    call. Eliminates the duplicated ``wrap_table_card(title, _build_rows(...), ...)``
    pattern in ``reached_signatures`` and ``total_initiatives``.

    Args:
        title:           HTML title string (e.g. ``<h3>…</h3>``).
        df:              Filtered and sorted DataFrame of initiatives.
        scrollbar_color: CSS colour value applied to the scroll wrapper.

    Returns:
        An HTML string wrapping everything in a ``card`` div.
    """
    return wrap_table_card(
        title,
        build_sig_threshold_rows(df),
        df,
        HEADERS_WITH_SIGNATURES,
        scrollbar_color,
    )
