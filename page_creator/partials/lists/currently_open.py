"""Renders a scrollable table of ECI initiatives currently open for signature collection."""

# Third party
import pandas as pd

# Local
from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, progress_bar, truncate

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

    open_df = df[df["current_status"] == _STATUS].copy()

    open_df["_start_dt"] = pd.to_datetime(
        open_df["timeline_collection_start"], dayfirst=True, errors="raise"
    )
    open_df["_has_closed"] = open_df["timeline_collection_closed"].notna() & (
        open_df["timeline_collection_closed"].str.strip() != ""
    )

    open_df = (
        open_df.sort_values(["_has_closed", "_start_dt"], ascending=[True, True])
        .drop(columns=["_start_dt", "_has_closed"])
        .reset_index(drop=True)
    )

    if open_df.empty:
        title = """\n\nNo initiatives currently open for signature collection.\n\n"""
        return wrap_card(title)

    rows = ""
    for _, row in open_df.iterrows():
        url = row["url"]
        objective = truncate(row["objective"])

        # --- Days Left cell ---
        date_start = row.get("timeline_collection_start", "")
        date_closed = row.get("timeline_collection_closed", "")
        date_start = "" if pd.isna(date_start) else str(date_start).strip()
        date_closed = "" if pd.isna(date_closed) else str(date_closed).strip()

        # Compute elapsed % of the 12-month window for the static progress bar
        if date_start:
            start_dt = pd.to_datetime(date_start, dayfirst=True, errors="coerce")
            deadline_dt = start_dt + pd.DateOffset(months=12)
            now_dt = pd.Timestamp.now()
            total_ms = (deadline_dt - start_dt).total_seconds()
            elapsed_ms = (now_dt - start_dt).total_seconds()
            pct = min(max(elapsed_ms / total_ms * 100, 0), 100)
            bar = progress_bar(pct, "days-left")
        else:
            bar = ""

        days_left = (
            f'<td class="days-left-cell" data-start="{date_start}" data-closed="{date_closed}">'
            f'<span class="days-left-cell__label"></span>'
            f"{bar}"
            f"</td>"
        )

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
            threshold = (
                f"{thr_val}"
                " / "
                f"{_COUNTRIES_THRESHOLD}{progress_bar(thr_val / _COUNTRIES_THRESHOLD * 100, 'threshold')}"
            )
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
