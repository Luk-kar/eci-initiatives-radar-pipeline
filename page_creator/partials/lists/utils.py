"""Shared HTML-generation helpers for list and table partials."""

# Third-party
import pandas as pd

# Local
from page_creator.utils import (
    wrap_card,
)

_DEFAULT_TRUNCATE = 100
_SCROLL_THRESHOLD = 5
_SIG_TARGET = 1_000_000
_COUNTRIES_THRESHOLD = 7


def truncate(text: str, max_len: int = _DEFAULT_TRUNCATE) -> str:
    """Truncate ``text`` to ``max_len`` characters, appending '…' if cut; returns '' for NaN."""
    if pd.isna(text):
        return ""
    s = str(text)
    return s if len(s) <= max_len else s[: max_len - 1] + "…"


def progress_bar(pct: float, modifier: str = "") -> str:
    """Return an HTML progress bar div filled to ``pct``%,
    capped at 100% visually with an over-threshold colour class if exceeded.
    """
    clamped = min(max(pct, 0.0), 100.0)
    over = pct > 100.0
    mod_class = f" progress-bar__fill--{modifier}" if modifier else ""
    over_class = " progress-bar__fill--over" if over else ""
    return (
        f'<div class="progress-bar">'
        f'<div class="progress-bar__fill{mod_class}{over_class}" style="width:{clamped:.1f}%">'
        f"</div></div>"
    )


def build_table(
    headers: list[str],
    rows_html: str,
    scrollable: bool = False,
    scrollbar_color: str | None = None,
) -> str:
    """Return an HTML ``data-table`` string with a sticky header row,
    optionally wrapped in a scrollable container div.

    Args:
        headers:         Column header labels.
        rows_html:       Pre-rendered ``<tr>`` HTML string.
        scrollable:      Whether to wrap the table in a scroll container.
        scrollbar_color: Optional hex colour applied as ``--scrollbar-color``
                         CSS variable on the scroll wrapper, overriding the default thumb colour.
    """
    header_cells = "\n      ".join(f"<th>{h}</th>" for h in headers)

    if scrollable:
        color_style = (
            f' style="--scrollbar-color:{scrollbar_color}"' if scrollbar_color else ""
        )
        wrapper_open = f'<div class="data-table__scroll-wrapper"{color_style}>'
        wrapper_close = "</div>"
    else:
        wrapper_open = ""
        wrapper_close = ""

    return f"""{wrapper_open}
<table class="data-table">
  <thead>
    <tr>
      {header_cells}
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>
{wrapper_close}"""


def normalise_registration_date(df: pd.DataFrame) -> pd.DataFrame:
    """Parse and normalise the ``registration_date`` column to ``datetime.date``.

    Args:
        df: DataFrame with a ``registration_date`` column in ``DD/MM/YYYY`` format.

    Returns:
        The same DataFrame with ``registration_date`` converted to ``datetime.date``.
    """
    df = df.copy()
    df["registration_date"] = pd.to_datetime(
        df["registration_date"], format="%d/%m/%Y"
    ).dt.date
    return df


def build_initiative_row(row: pd.Series, extra_cells: str = "") -> str:
    """Return a ``<tr>`` with the common Initiative / Registration / Objective cells.

    Args:
        row:         A DataFrame row. Must contain ``title``, ``url``,
                     ``registration_date``, and ``objective``.
        extra_cells: Additional ``<td>`` HTML appended after the three base cells.

    Returns:
        A ``<tr>...</tr>`` HTML string.
    """
    url = row.get("url") or "#"
    registration = row["registration_date"]
    objective = truncate(row.get("objective", ""))
    return f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{row["title"]}</a></td>
          <td>{registration}</td>
          <td>{objective}</td>{extra_cells}
        </tr>"""


def wrap_table_card(
    title: str,
    rows: str,
    df: pd.DataFrame,
    headers: list[str],
    scrollbar_color: str,
) -> str:
    """Wrap a title and pre-rendered table rows in a scrollable card.

    Args:
        title:           HTML title string (e.g. ``<h3>…</h3>``).
        rows:            Concatenated ``<tr>`` HTML strings.
        df:              The filtered DataFrame, used to determine scroll threshold.
        headers:         Column header labels passed to ``build_table``.
        scrollbar_color: CSS colour value applied to the scroll wrapper.

    Returns:
        An HTML string wrapping everything in a ``card`` div.
    """

    return wrap_card(
        title
        + build_table(
            headers,
            rows,
            scrollable=len(df) > _SCROLL_THRESHOLD,
            scrollbar_color=scrollbar_color,
        )
    )


def sig_cell(value) -> str:
    """Return formatted signatures cell content with progress bar, or ``N/A``.

    Args:
        value: Raw ``signatures_collected`` value from a DataFrame row.

    Returns:
        An HTML string for the signatures table cell content (without ``<td>`` tags).
    """
    if pd.notna(value):
        sig_val = int(value)
        return f"{sig_val:,}{progress_bar(sig_val / _SIG_TARGET * 100, 'signatures')}"
    return "N/A"


def threshold_cell(value) -> str:
    """Return formatted countries-threshold cell content with progress bar, or ``N/A``.

    Args:
        value: Raw ``signatures_threshold_met`` value from a DataFrame row.

    Returns:
        An HTML string for the threshold table cell content (without ``<td>`` tags).
    """
    if pd.notna(value):
        thr_val = int(value)
        return (
            f"{thr_val} / {_COUNTRIES_THRESHOLD}"
            f"{progress_bar(thr_val / _COUNTRIES_THRESHOLD * 100, 'threshold')}"
        )
    return "N/A"
