"""Renders a scrollable table of ECI initiatives that received an EU Commission response."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, truncate


_RESPONSE_STATUSES = frozenset(
    ["Commission Engaged", "Law Passed", "Rejected Legislation"]
)
_SCROLL_THRESHOLD = 5

_HEADERS = ["Initiative", "Objective", "Response"]


def generate_got_response(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that received a Commission response.

    Filters for rows with ``current_status`` in ``_RESPONSE_STATUSES``, sorted by
    signature count descending. Each row shows the initiative title (linked to
    its page), a truncated objective, and the truncated commission response text.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, and ``commission_answer_text`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives received a response.
    """

    filtered_df = (
        df[df["current_status"].isin(_RESPONSE_STATUSES)]
        .sort_values("signatures_collected", ascending=False)
        .reset_index(drop=True)
    )

    title = f'<h3 class="card__title">📬 Got EU Response: <span class="card__count">{len(filtered_df)}</span></h3>'

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have received an EU Commission response.</p>'
        return wrap_card(title + body)

    rows = ""
    for _, row in filtered_df.iterrows():
        url = row.get("url") or "#"
        objective = truncate(row.get("objective", ""))
        response = truncate(row.get("commission_answer_text", ""), max_len=200)

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{objective}</td>
          <td>{response}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(_HEADERS, rows, scrollable=len(filtered_df) > _SCROLL_THRESHOLD)
    )
