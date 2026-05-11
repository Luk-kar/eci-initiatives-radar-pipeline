import ast

import pandas as pd

from page_creator.partials.lists.utils import (
    build_card_title,
    build_initiative_row,
    normalise_registration_date,
    truncate,
    wrap_table_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date
from page_creator.utils import wrap_card
from page_creator.partials.lists.utils.text import (
    strip_boilerplate_headers,
    strip_markdown_links,
)

STATUS = "Law Passed"
HEADERS = ("Initiative", "Registration", "Objective", "Legislation Example")


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives with Law Passed status."""
    return df[df["current_status"] == STATUS]


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending."""
    return sort_by_registration_date(df)


def _parse_last_legislation(raw) -> str:
    """Return the last item from a stringified list, or empty string."""
    if not raw or pd.isna(raw):
        return ""
    try:
        items = ast.literal_eval(str(raw))
    except (ValueError, SyntaxError):
        return ""
    if not isinstance(items, list) or not items:
        return ""
    return items[-1]


def _build_row(row: pd.Series) -> str:
    """Return a <tr> for a single initiative that led to passed legislation.

    Args:
        row: A DataFrame row. Must contain title, initiative_url,
             registration)date, objective, and law_passed.

    Returns:
        A <tr>...</tr> HTML string.
    """
    # Legislation
    last = _parse_last_legislation(row["law_passed"])

    legislation = None

    if last:
        salinized = strip_boilerplate_headers(strip_markdown_links(last))
        legislation = truncate(salinized, 150)
    else:
        legislation = ""

    # Objective
    row = row.copy()
    row["objective"] = strip_markdown_links(row["objective"])

    return build_initiative_row(row, f"<td>{legislation}</td>")


def _build_rows(filtered_df: pd.DataFrame) -> str:
    """Iterate over all matching initiatives and concatenate their row HTML.

    Args:
        filtered_df: Filtered and sorted DataFrame.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(_build_row(row) for _, row in filtered_df.iterrows())


def generate_law_passed(df: pd.DataFrame) -> str:
    """
    Return an HTML card containing a table of ECIs that led to passed legislation.

    Filters for rows with ``current_status == "Law Passed"``, sorted by
    registration date descending.  The "Legislation Example" column shows the
    *last* entry from the ``law_passed`` list — the most recently recorded
    piece of legislation linked to the initiative — truncated to fit.

    Args:
        df: The full ECI initiatives DataFrame.  Must contain
            ``current_status``, ``title``, ``initiative_url``, ``objective``,
            ``registration_date``, and ``law_passed`` columns.

    Returns:
        An HTML string wrapping the table in a card div, or a card with a
        fallback message if no initiatives have law passed.
    """
    df_filtered = _filter(df)
    df_sorted = _sort(df_filtered)
    df_final = normalise_registration_date(df_sorted)

    color = colors.law_passed
    title = build_card_title("⚖️", STATUS, len(df_final), color)

    if df_final.empty:
        return wrap_card(
            f"{title}<p class='list-empty'>No initiatives have led to passed legislation yet.</p>"
        )

    return wrap_table_card(title, _build_rows(df_final), df_final, HEADERS, color)
