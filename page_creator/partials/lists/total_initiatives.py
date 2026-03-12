"""Renders a scrollable table of all registered ECI initiatives."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, progress_bar, truncate


_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7
_SIG_TARGET = 1_000_000

_HEADERS = ["Initiative", "Objective", "Signatures", "Countries Threshold"]


def generate_total_initiatives(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of all registered ECI initiatives.

    Sorted by signature count descending. Each row shows the initiative title
    (linked to its page), a truncated objective, a signature progress bar towards
    the 1M target, and a country-threshold progress bar out of ``_COUNTRIES_THRESHOLD``.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``title``, ``url``,
            ``objective``, ``signatures_collected``, and ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div.
    """
    sorted_df = df.sort_values("signatures_collected", ascending=False).reset_index(
        drop=True
    )

    title = f'<h3 class="card__title">📋 Total Initiatives: <span class="card__count">{len(sorted_df)}</span></h3>'

    rows = ""
    for _, row in sorted_df.iterrows():

        url = row.get("url") or "#"
        objective = truncate(row.get("objective", ""))

        if pd.notna(row["signatures_collected"]):
            sig_val = int(row["signatures_collected"])
            sigs = (
                f"{sig_val:,}{progress_bar(sig_val / _SIG_TARGET * 100, 'signatures')}"
            )
        else:
            sigs = "N/A"

        if pd.notna(row["signatures_threshold_met"]):
            thr_val = int(row["signatures_threshold_met"])
            threshold = f"{thr_val} / {_COUNTRIES_THRESHOLD}{progress_bar(thr_val / _COUNTRIES_THRESHOLD * 100, 'threshold')}"
        else:
            threshold = "N/A"

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{objective}</td>
          <td>{sigs}</td>
          <td>{threshold}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(_HEADERS, rows, scrollable=len(sorted_df) > _SCROLL_THRESHOLD)
    )
