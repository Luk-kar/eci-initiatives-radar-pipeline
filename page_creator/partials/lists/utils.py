"""Shared HTML-generation helpers for list and table partials."""

# Third-party
import pandas as pd

_DEFAULT_TRUNCATE = 100
_DEFAULT_SCROLL_THRESHOLD = 5


def truncate(text: str, max_len: int = _DEFAULT_TRUNCATE) -> str:
    """
    Truncate ``text`` to ``max_len`` characters, appending '…' if cut; returns '' for NaN.
    """

    if pd.isna(text):
        return ""

    s = str(text)

    return s if len(s) <= max_len else s[: max_len - 1] + "…"


def progress_bar(pct: float, modifier: str = "") -> str:
    """
    Return an HTML progress bar div filled to ``pct``%,
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


def build_table(headers: list[str], rows_html: str, scrollable: bool = False) -> str:
    """
    Return an HTML ``data-table`` string with a sticky header row,
    optionally wrapped in a scrollable container div.
    """

    header_cells = "\n      ".join(f"<th>{h}</th>" for h in headers)
    wrapper_open = '<div class="data-table__scroll-wrapper">' if scrollable else ""
    wrapper_close = "</div>" if scrollable else ""
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
