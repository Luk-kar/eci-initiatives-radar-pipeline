"""Renders a scrollable table of ECI initiatives currently open for signature collection."""

# Third party
import pandas as pd

# Local
from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, progress_bar, truncate
from page_creator.partials.styles.colors import kpi_colors as colors

_STATUS = "Collection Ongoing"
_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7
_SIG_TARGET = 1_000_000

_HEADERS = ["Initiative", "Objective", "Days Left", "Signatures", "Countries Threshold"]


def generate_currently_open(df: pd.DataFrame) -> str:
    """
    Return an HTML card containing a table of all currently open ECI initiatives.

    Filters for rows with ``current_status == 'Collection Ongoing'``, sorted by
    signature count descending. Each row shows the initiative title (linked to its
    page), a truncated objective, a days-left cell (JavaScript-rendered from
    ``timeline_collection_start`` and ``timeline_collection_closed``), a signature
    progress bar towards the 1M target, and a country-threshold progress bar out of
    ``_COUNTRIES_THRESHOLD``.

    The table gains a scroll wrapper when the row count exceeds ``_SCROLL_THRESHOLD``.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``signatures_collected``,
            ``signatures_threshold_met``, ``timeline_collection_start``, and
            ``timeline_collection_closed`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives are currently open.
    """
    open_df = (
        df[df["current_status"] == _STATUS]
        .sort_values("signatures_collected", ascending=False)
        .reset_index(drop=True)
    )

    if open_df.empty:
        title = f"""\n\nNo initiatives currently open for signature collection.\n\n"""
        return wrap_card(title)

    rows = ""
    for _, row in open_df.iterrows():
        url = row.get("url") or "#"
        objective = truncate(row.get("objective", ""))

        # --- Days Left cell ---
        date_start = row.get("timeline_collection_start", "")
        date_closed = row.get("timeline_collection_closed", "")
        date_start = "" if pd.isna(date_start) else str(date_start)
        date_closed = "" if pd.isna(date_closed) else str(date_closed)
        days_left = f"""<td class="days-left-cell" data-start="{date_start}" data-closed="{date_closed}"></td>"""

        # --- Signatures cell ---
        if pd.notna(row["signatures_collected"]):
            sig_val = int(row["signatures_collected"])
            sigs = (
                f"{sig_val:,}{progress_bar(sig_val / _SIG_TARGET * 100, 'signatures')}"
            )
        else:
            sigs = "N/A"

        # --- Countries threshold cell ---
        if pd.notna(row["signatures_threshold_met"]):
            thr_val = int(row["signatures_threshold_met"])
            threshold = f"{thr_val} / {_COUNTRIES_THRESHOLD}{progress_bar(thr_val / _COUNTRIES_THRESHOLD * 100, 'threshold')}"
        else:
            threshold = "N/A"

        rows += f"""
        <tr>
            <td><a href="{url}" target="_blank">{row.get('title', '')}</a></td>
            <td>{objective}</td>
            {days_left}
            <td>{sigs}</td>
            <td>{threshold}</td>
        </tr>"""

    body = build_table(_HEADERS, rows, scrollable=len(open_df) > _SCROLL_THRESHOLD)
    title = f"""\n\nCurrently Open ({len(open_df)})\n\n"""
    return wrap_card(title + body)
