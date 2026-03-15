"""Renders a scrollable table of ECI initiatives that received an EU Commission response."""

import pandas as pd

from page_creator.utils import wrap_card
from page_creator.partials.lists.utils import (
    build_initiative_row,
    normalise_registration_date,
    truncate,
    wrap_table_card,
)
from page_creator.partials.styles.colors import kpi_colors as colors

_RESPONSE_STATUSES = frozenset(
    ["Commission Engaged", "Law Passed", "Rejected Legislation"]
)
_HEADERS = ["Initiative", "Registration", "Objective", "Response"]


def _filter_and_sort(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that received a Commission response, sorted by registration date.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered and sorted DataFrame containing only ``_RESPONSE_STATUSES`` rows.
    """
    return normalise_registration_date(
        df[df["current_status"].isin(_RESPONSE_STATUSES)]
        .sort_values("registration_date", ascending=False)
        .reset_index(drop=True)
    )


def _build_row(row: pd.Series) -> str:
    """Return a ``<tr>`` for a single initiative with a Commission response.

    Args:
        row: A DataFrame row. Must contain ``title``, ``url``, ``registration_date``,
             ``objective``, and ``commission_answer_text``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    response = truncate(row["commission_answer_text"], max_len=200)
    return build_initiative_row(row, f"\n          <td>{response}</td>")


def _build_rows(filtered_df: pd.DataFrame) -> str:
    """Iterate over all matching initiatives and concatenate their row HTML.

    Args:
        filtered_df: Filtered and sorted DataFrame.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(_build_row(row) for _, row in filtered_df.iterrows())


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
    filtered_df = _filter_and_sort(df)

    title = (
        '<h3 class="card__title">'
        "📬 Got EU Response: "
        f'<span class="card__count" style="color:{colors.got_response}">{len(filtered_df)}</span>'
        "</h3>"
    )

    if filtered_df.empty:
        body = '<p class="list-empty">No initiatives have received an EU Commission response.</p>'
        return wrap_card(title + body)

    return wrap_table_card(
        title, _build_rows(filtered_df), filtered_df, _HEADERS, colors.got_response
    )
