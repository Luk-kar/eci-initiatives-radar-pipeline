import pandas as pd

_DEFAULT_TRUNCATE = 100
_DEFAULT_SCROLL_THRESHOLD = 5


def truncate(text: str, max_len: int = _DEFAULT_TRUNCATE) -> str:
    if pd.isna(text):
        return ""
    s = str(text)
    return s if len(s) <= max_len else s[: max_len - 1] + "…"


def progress_bar(pct: float, modifier: str = "") -> str:
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
