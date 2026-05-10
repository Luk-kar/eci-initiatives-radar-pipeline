"""Renders a scrollable table of ECI initiatives Collection Ongoing for signature collection."""

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
from page_creator.partials.styles.colors import kpi_colors as colors
from page_creator.partials.lists.utils.text import wrap_initiative_title

_STATUS = "Collection Ongoing"
_HEADERS = ["Initiative", "Objective", "Days Left", "Signatures", "Countries Threshold"]


def _filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives with ``_STATUS`` status.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only ``_STATUS`` rows.
    """
    return df[df["current_status"] == _STATUS].copy()


def _sort(df: pd.DataFrame) -> pd.DataFrame:
    """Sort open initiatives by start date ascending, with closed ones pushed last.

    Args:
        df: Filtered DataFrame of open initiatives.

    Returns:
        Sorted DataFrame with temporary helper columns dropped.
    """
    df["_start_dt"] = pd.to_datetime(
        df["timeline_collection_start"], dayfirst=True, errors="raise"
    )
    df["_has_closed"] = df["timeline_collection_closed"].notna() & (
        df["timeline_collection_closed"].str.strip() != ""
    )

    return (
        df.sort_values(["_has_closed", "_start_dt"], ascending=[True, True])
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

    Args:
        row: A DataFrame row. Must contain ``title``, ``initiative_url``, ``objective``,
             ``timeline_collection_start``, ``timeline_collection_closed``,
             ``signatures_collected``, and ``signatures_countries_threshold_met_count``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    title = wrap_initiative_title(row["title"])
    initiative_url = row.get("initiative_url") or "#"
    objective = truncate(row.get("objective", ""))

    date_start = row.get("timeline_collection_start", "")
    date_closed = row.get("timeline_collection_closed", "")
    date_start = "" if pd.isna(date_start) else str(date_start).strip()
    date_closed = "" if pd.isna(date_closed) else str(date_closed).strip()

    return f"""
        <tr>
          <td><a href="{initiative_url}" target="_blank" rel="noopener noreferrer">{title}</a></td>
          <td>{objective}</td>
          {_days_left_cell(date_start, date_closed)}
          <td>{sig_cell(row["signatures_collected"])}</td>
          <td>{threshold_cell(row["signatures_countries_threshold_met_count"])}</td>
        </tr>"""


def _build_rows(open_df: pd.DataFrame) -> str:
    """Iterate over all open initiatives and concatenate their row HTML.

    Args:
        open_df: Filtered and sorted DataFrame of open initiatives.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(_build_row(row) for _, row in open_df.iterrows())


def generate_collection_ongoing(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of all Collection Ongoing ECI initiatives.

    Filters for rows with ``current_status == 'Collection Ongoing'``, sorted by
    collection start date ascending, with closed initiatives pushed to the bottom.
    Each row shows the initiative title (linked to its page), a truncated objective,
    a JavaScript-rendered days-left cell, a signature progress bar, and a
    country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``initiative_url``, ``objective``, ``signatures_collected``,
            ``signatures_countries_threshold_met_count``, ``timeline_collection_start``, and
            ``timeline_collection_closed`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives are collection ongoing.
    """

    df_filter = _filter(df)
    df_open = _sort(df_filter)

    if df_open.empty:
        return wrap_card(
            "\n\nNo initiatives collection ongoing for signature collection.\n\n"
        )

    title = (
        '<h3 class="card__title">🗳️ Collection Ongoing:'
        "<span "
        f'class="card__count" style="color:{colors.collection_ongoing}">{len(df_open)}'
        "</span>"
        "</h3>"
    )

    body = build_table(
        _HEADERS, _build_rows(df_open), scrollable=len(df_open) > SCROLL_THRESHOLD
    )

    return wrap_card(title + body)
