"""Renders a scrollable table of ECI initiatives currently open for signature collection."""

# Third-party
import pandas as pd

# Local
from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    build_table,
    progress_bar,
    sig_cell,
    threshold_cell,
    truncate,
    SCROLL_THRESHOLD,
)

_STATUS = "Collection Ongoing"
_HEADERS = ["Initiative", "Objective", "Days Left", "Signatures", "Countries Threshold"]


def _filter_and_sort(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for open initiatives and sort by start date, closed ones last.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered and sorted DataFrame containing only ``_STATUS`` rows.
    """

    open_df = df[df["current_status"] == _STATUS].copy()

    open_df["_start_dt"] = pd.to_datetime(
        open_df["timeline_collection_start"], dayfirst=True, errors="raise"
    )
    open_df["_has_closed"] = open_df["timeline_collection_closed"].notna() & (
        open_df["timeline_collection_closed"].str.strip() != ""
    )

    return (
        open_df.sort_values(["_has_closed", "_start_dt"], ascending=[True, True])
        .drop(columns=["_start_dt", "_has_closed"])
        .reset_index(drop=True)
    )


def _days_left_cell(date_start: str, date_closed: str) -> str:
    """Return a ``<td>`` element containing the JS-rendered days-left label and progress bar.

    Args:
        date_start:  Collection start date string (DD/MM/YYYY), or empty string.
        date_closed: Collection closed date string (DD/MM/YYYY), or empty string.

    Returns:
        A ``<td class="days-left-cell">`` HTML string.
    """
    if date_start:

        start_dt = pd.to_datetime(date_start, dayfirst=True, errors="coerce")
        deadline_dt = start_dt + pd.DateOffset(months=12)
        now_dt = pd.Timestamp.now()

        total_secs = (deadline_dt - start_dt).total_seconds()
        elapsed_secs = (now_dt - start_dt).total_seconds()

        pct = min(max(elapsed_secs / total_secs * 100, 0), 100)
        bar = progress_bar(pct, "days-left")
    else:
        bar = ""

    return (
        f'<td class="days-left-cell" data-start="{date_start}" data-closed="{date_closed}">'
        f'<span class="days-left-cell__label"></span>'
        f"{bar}"
        f"</td>"
    )


def _build_row(row: pd.Series) -> str:
    """Return a fully assembled ``<tr>`` for a single open initiative.

    The ``sig_cell`` and ``threshold_cell`` from ``utils`` return content-only strings
    (no ``<td>`` tags), so they are wrapped here. The days-left cell is unique to this
    module and built via ``_days_left_cell``.

    Args:
        row: A DataFrame row. Must contain ``title``, ``url``, ``objective``,
             ``timeline_collection_start``, ``timeline_collection_closed``,
             ``signatures_collected``, and ``signatures_threshold_met``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    url = row.get("url") or "#"
    objective = truncate(row.get("objective", ""))

    date_start = row.get("timeline_collection_start", "")
    date_closed = row.get("timeline_collection_closed", "")
    date_start = "" if pd.isna(date_start) else str(date_start).strip()
    date_closed = "" if pd.isna(date_closed) else str(date_closed).strip()

    return f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{objective}</td>
          {_days_left_cell(date_start, date_closed)}
          <td>{sig_cell(row["signatures_collected"])}</td>
          <td>{threshold_cell(row["signatures_threshold_met"])}</td>
        </tr>"""


def _build_rows(open_df: pd.DataFrame) -> str:
    """Iterate over all open initiatives and concatenate their row HTML.

    Args:
        open_df: Filtered and sorted DataFrame of open initiatives.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(_build_row(row) for _, row in open_df.iterrows())


def generate_currently_open(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of all currently open ECI initiatives.

    Filters for rows with ``current_status == 'Collection Ongoing'``, sorted by
    collection start date ascending, with closed initiatives pushed to the bottom.
    Each row shows the initiative title (linked to its page), a truncated objective,
    a JavaScript-rendered days-left cell, a signature progress bar, and a
    country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``signatures_collected``,
            ``signatures_threshold_met``, ``timeline_collection_start``, and
            ``timeline_collection_closed`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives are currently open.
    """
    open_df = _filter_and_sort(df)

    if open_df.empty:
        return wrap_card(
            "\n\nNo initiatives currently open for signature collection.\n\n"
        )

    title = f"\n\nCurrently Open ({len(open_df)})\n\n"
    body = build_table(
        _HEADERS, _build_rows(open_df), scrollable=len(open_df) > SCROLL_THRESHOLD
    )

    return wrap_card(title + body)
