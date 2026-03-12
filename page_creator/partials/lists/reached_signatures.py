"""Renders a scrollable table of ECI initiatives that reached the 1M signature threshold."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, progress_bar, truncate
from page_creator.partials.styles.colors import kpi_colors as colors


_SIG_TARGET = 1_000_000
_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7

_HEADERS = ["Initiative", "Objective", "Signatures", "Countries Threshold"]


def generate_reached_signatures(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that reached 1M signatures.

    Filters for rows where ``signatures_collected >= 1_000_000``, sorted by
    signature count descending. Each row shows the initiative title (linked to
    its page), a truncated objective, a signature progress bar, and a
    country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``signatures_collected``,
            ``title``, ``url``, ``objective``, and ``signatures_threshold_met`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives reached the threshold.
    """

    filtered_df = (
        df[df["signatures_collected"] >= _SIG_TARGET]
        .sort_values("signatures_collected", ascending=False)
        .reset_index(drop=True)
    )

    title = f'<h3 class="card__title">✅ Reached 1M Signatures: <span class="card__count" style="color:{colors.reached_signatures}">{len(filtered_df)}</span></h3>'

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have reached 1M signatures.</p>'
        return wrap_card(title + body)

    rows = ""
    for _, row in filtered_df.iterrows():
        url = row.get("url") or "#"
        objective = truncate(row.get("objective", ""))

        sig_val = int(row["signatures_collected"])
        sigs = f"{sig_val:,}{progress_bar(sig_val / _SIG_TARGET * 100, 'signatures')}"

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
        + build_table(
            _HEADERS,
            rows,
            scrollable=len(filtered_df) > _SCROLL_THRESHOLD,
            scrollbar_color=colors.reached_signatures,
        )
    )
