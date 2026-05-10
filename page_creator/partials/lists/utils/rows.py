"""Shared HTML row and cell builders for ECI initiative tables."""

import pandas as pd

from page_creator.partials.lists.utils.signatures import sig_cell, threshold_cell
from page_creator.partials.lists.utils.table import wrap_table_card
from page_creator.partials.lists.utils.text import (
    truncate,
    wrap_initiative_title,
    strip_markdown_links,
    strip_boilerplate_headers,
)
from page_creator.partials.lists.utils.dates import normalise_registration_date
from page_creator.utils import wrap_card

# Shared column headers for tables that include signature and threshold columns
HEADERS_WITH_SIGNATURES = [
    "Initiative",
    "Registration",
    "Objective",
    "Signatures",
    "Countries Threshold",
]


def build_initiative_row(row: pd.Series, extra_cells: str = "") -> str:
    """Return a ``<tr>`` with the common Initiative / Registration / Objective cells.

    Args:
        row:         A DataFrame row. Must contain ``title``, ``initiative_url``,
                     ``registration_date``, and ``objective``.
        extra_cells: Additional ``<td>`` HTML appended after the three base cells.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    # title = row["title"]
    title = wrap_initiative_title(row["title"])
    initiative_url = row["initiative_url"]
    registration = row["registration_date"]
    objective = strip_markdown_links(truncate(row["objective"]))

    return f"""
        <tr>
          <td><a href="{initiative_url}" target="_blank" rel="noopener noreferrer">{title}</a></td>
          <td>{registration}</td>
          <td>{objective}</td>{extra_cells}
        </tr>"""


def build_sig_threshold_row(row: pd.Series) -> str:
    """Return a ``<tr>`` with Initiative / Registration / Objective / Signatures / Threshold cells.

    Shared by ``reached_signatures`` and ``total_initiatives`` which have identical
    row structure. Eliminates the duplicated ``_build_row`` in both modules.

    Args:
        row: A DataFrame row. Must contain ``title``, ``initiative_url``, ``registration_date``,
             ``objective``, ``signatures_collected``, and ``signatures_countries_threshold_met_count``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    extra = (
        f"\n          <td>{sig_cell(row['signatures_collected'])}</td>"
        f"\n          <td>{threshold_cell(row['signatures_countries_threshold_met_count'])}</td>"
    )
    return build_initiative_row(row, extra)


def build_sig_threshold_rows(df: pd.DataFrame) -> str:
    """Iterate over a DataFrame and concatenate ``<tr>`` HTML for each row.

    Shared by ``reached_signatures`` and ``total_initiatives``.

    Args:
        df: DataFrame of initiatives. Each row is passed to ``build_sig_threshold_row``.

    Returns:
        Concatenated ``<tr>`` HTML string for all rows.
    """
    return "".join(build_sig_threshold_row(row) for _, row in df.iterrows())


def build_response_row(row: pd.Series) -> str:
    """Return a ``<tr>`` for an initiative with a truncated Commission response cell.

    Shared by ``commission_engaged``, ``rejected_legislation``, and ``got_response``.

    Args:
        row: Must contain ``title``, ``initiative_url``, ``registration_date``,
             ``objective``, and ``commission_answer``.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    removed_links = strip_markdown_links(row["commission_answer"])

    no_boilerplate = strip_boilerplate_headers(removed_links)
    response = truncate(no_boilerplate, max_len=200)

    return build_initiative_row(row, f"\n          <td>{response}</td>")


def build_response_rows(df: pd.DataFrame) -> str:
    """Iterate over a DataFrame and concatenate response ``<tr>`` HTML for each row."""
    return "".join(build_response_row(row) for _, row in df.iterrows())


def generate_response_card(
    df: pd.DataFrame,
    title: str,
    headers: list[str],
    color: str,
    empty_message: str,
) -> str:
    """Run the standard filter→sort→normalise→render pipeline for response-type lists.

    Shared by ``commission_engaged``, ``rejected_legislation``, and ``got_response``.

    Args:
        df:            Already-filtered and sorted DataFrame (normalise not yet applied).
        title:         Pre-rendered ``<h3>`` HTML title string.
        headers:       Column header labels.
        color:         CSS colour for the scrollbar.
        empty_message: Fallback ``<p>`` message text when ``df`` is empty.

    Returns:
        An HTML string wrapping the table in a ``card`` div.
    """

    df_final = normalise_registration_date(df)

    if df_final.empty:
        return wrap_card(title + f'<p class="list-empty">{empty_message}</p>')

    return wrap_table_card(
        title, build_response_rows(df_final), df_final, headers, color
    )


def wrap_sig_threshold_card(
    title: str,
    df: pd.DataFrame,
    scrollbar_color: str,
) -> str:
    """Render a complete signatures+threshold card from a filtered DataFrame.

    Combines ``build_sig_threshold_rows`` and ``wrap_table_card`` into a single
    call. Eliminates the duplicated ``wrap_table_card(title, _build_rows(...), ...)``
    pattern in ``reached_signatures`` and ``total_initiatives``.

    Args:
        title:           HTML title string (e.g. ``<h3>…</h3>``).
        df:              Filtered and sorted DataFrame of initiatives.
        scrollbar_color: CSS colour value applied to the scroll wrapper.

    Returns:
        An HTML string wrapping everything in a ``card`` div.
    """
    return wrap_table_card(
        title,
        build_sig_threshold_rows(df),
        df,
        HEADERS_WITH_SIGNATURES,
        scrollbar_color,
    )


# ── Title builder ─────────────────────────────────────────────────────────────


def build_card_title(emoji: str, label: str, count: int, color: str) -> str:
    """Return a ``<h3 class="card__title">`` HTML string with a coloured count badge.

    Shared by every list partial to eliminate repeated f-string boilerplate.

    Args:
        emoji:  Leading emoji character(s), e.g. ``"🏛️"``.
        label:  Status label shown after the emoji, e.g. ``"Commission Engaged"``.
        count:  Number of initiatives, rendered inside the coloured ``<span>``.
        color:  CSS colour value for the count span.

    Returns:
        A ``<h3>…</h3>`` HTML string.
    """
    return (
        f'<h3 class="card__title">{emoji} {label}: '
        f'<span class="card__count" style="color:{color}">{count}</span>'
        "</h3>"
    )


# ── Sig-threshold card pipeline ────────────────────────────────────────────────


def generate_sig_threshold_card(
    df: pd.DataFrame,
    title: str,
    color: str,
    empty_message: str,
) -> str:
    """Run the standard filter→sort→normalise→render pipeline for sig-threshold lists.

    Shared by ``awaiting_response``, ``collection_unsuccessful``, ``withdrawn``,
    and ``reached_signatures``.

    Args:
        df:            Already-filtered and sorted DataFrame (normalise not yet applied).
        title:         Pre-rendered ``<h3>`` HTML title string.
        color:         CSS colour for the scrollbar / count span.
        empty_message: Fallback message text when ``df`` is empty.

    Returns:
        An HTML string wrapping the table in a ``card`` div.
    """
    df_final = normalise_registration_date(df)

    if df_final.empty:
        return wrap_card(title + f'<p class="list-empty">{empty_message}</p>')

    return wrap_sig_threshold_card(title, df_final, color)
