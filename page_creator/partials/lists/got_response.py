"""Renders a scrollable table of ECI initiatives that received an EU Commission response."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, truncate
from page_creator.partials.styles.colors import kpi_colors as colors


_RESPONSE_STATUSES = frozenset(
    ["Commission Engaged", "Law Passed", "Rejected Legislation"]
)
_SCROLL_THRESHOLD = 5

_HEADERS = ["Initiative", "Registration", "Objective", "Response"]


def generate_got_response(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that received a Commission response.

    Filters for rows with ``current_status`` in ``_RESPONSE_STATUSES``, sorted by
    registration date descending. Each row shows the initiative title (linked to
    its page), the registration date, a truncated objective, and the truncated
    commission response text.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, ``registration_date``, and
            ``commission_answer_text`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives received a response.
    """

    filtered_df = (
        df[df["current_status"].isin(_RESPONSE_STATUSES)]
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )

    title = (
        '<h3 class="card__title">'
        "📬 Got EU Response: "
        f'<span class="card__count" style="color:{colors.got_response}">{len(filtered_df)}</span>'
        "</h3>"
    )

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have received an EU Commission response.</p>'
        return wrap_card(title + body)

    df["registration_date"] = pd.to_datetime(
        df["registration_date"], format="%d/%m/%Y"
    ).dt.date

    rows = ""
    for _, row in filtered_df.iterrows():

        url = row["url"]
        registration = row["registration_date"]
        objective = truncate(row["objective"])
        response = truncate(row["commission_answer_text"], max_len=200)

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{registration}</td>
          <td>{objective}</td>
          <td>{response}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(
            _HEADERS,
            rows,
            scrollable=len(filtered_df) > _SCROLL_THRESHOLD,
            scrollbar_color=colors.got_response,
        )
    )
