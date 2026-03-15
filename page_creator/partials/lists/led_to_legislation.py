"""Renders a scrollable table of ECI initiatives that directly led to EU legislation."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import build_table, truncate
from page_creator.partials.styles.colors import kpi_colors as colors

_STATUS = "Law Passed"
_SCROLL_THRESHOLD = 5
_LEGISLATION_FALLBACK = "Legislation details not yet available."

_HEADERS = ["Initiative", "Registration", "Objective", "Legislation"]


def generate_led_to_legislation(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that led to passed legislation.

    Filters for rows with ``current_status == 'Law Passed'``, sorted by
    registration date descending. The Legislation column uses a fallback
    placeholder until real legislative reference data is added to the dataset.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``,
            ``title``, ``url``, ``objective``, and ``registration_date`` columns.

    Returns:
        An HTML string wrapping the table in a ``card`` div, or a card with a
        fallback message if no initiatives led to legislation.
    """

    filtered_df = (
        df[df["current_status"] == _STATUS]
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )

    title = f'<h3 class="card__title">⚖️ Led to Legislation: <span class="card__count" style="color:{colors.led_to_legislation}">{len(filtered_df)}</span></h3>'

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have led to legislation yet.</p>'
        return wrap_card(title + body)

    df["registration_date"] = pd.to_datetime(
        df["registration_date"], format="%d/%m/%Y"
    ).dt.date

    rows = ""
    for _, row in filtered_df.iterrows():
        url = row["url"]
        registration = row["registration_date"]
        objective = truncate(row["objective"])

        # TODO: replace fallback once legislation column is added to the dataset
        legislation = truncate(row.get("legislation", _LEGISLATION_FALLBACK))

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{registration}</td>
          <td>{objective}</td>
          <td>{legislation}</td>
        </tr>"""

    return wrap_card(
        title
        + build_table(
            _HEADERS,
            rows,
            scrollable=len(filtered_df) > _SCROLL_THRESHOLD,
            scrollbar_color=colors.led_to_legislation,
        )
    )
