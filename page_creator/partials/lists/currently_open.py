import pandas as pd

from page_creator.utils import wrap_card


_STATUS = "Collection Ongoing"
_TRUNCATE = 100
_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7
_SIG_TARGET = 1_000_000


def _truncate(text: str, max_len: int = _TRUNCATE) -> str:
    if pd.isna(text):
        return ""
    s = str(text)
    return s if len(s) <= max_len else s[: max_len - 1] + "…"


def _progress_bar(pct: float, modifier: str = "") -> str:
    clamped = min(max(pct, 0.0), 100.0)
    over = pct > 100.0
    mod_class = f" progress-bar__fill--{modifier}" if modifier else ""
    over_class = " progress-bar__fill--over" if over else ""
    return (
        f'<div class="progress-bar">'
        f'<div class="progress-bar__fill{mod_class}{over_class}" style="width:{clamped:.1f}%">'
        f"</div></div>"
    )


def generate_currently_open(df: pd.DataFrame) -> str:
    open_df = (
        df[df["current_status"] == _STATUS]
        .sort_values("signatures_collected", ascending=False)
        .reset_index(drop=True)
    )

    title = f'<h3 class="card__title">🗳️ Currently Open: <span class="card__count">{len(open_df)}</span></h3>'

    if open_df.empty:
        body = '<p class="list-empty">No initiatives currently open for signature collection.</p>'
        return wrap_card(title + body)

    rows = ""
    for _, row in open_df.iterrows():
        url = row.get("url") or "#"
        name = row["title"]
        objective = _truncate(row.get("objective", ""))

        if pd.notna(row["signatures_collected"]):
            sig_val = int(row["signatures_collected"])
            sig_pct = sig_val / _SIG_TARGET * 100
            sigs = f"{sig_val:,}{_progress_bar(sig_pct, 'signatures')}"
        else:
            sigs = "N/A"

        if pd.notna(row["signatures_threshold_met"]):
            thr_val = int(row["signatures_threshold_met"])
            thr_pct = thr_val / _COUNTRIES_THRESHOLD * 100
            threshold = f"{thr_val} / {_COUNTRIES_THRESHOLD}{_progress_bar(thr_pct, 'threshold')}"
        else:
            threshold = "N/A"

        rows += f"""
        <tr>
          <td><a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a></td>
          <td>{objective}</td>
          <td>{sigs}</td>
          <td>{threshold}</td>
        </tr>"""

    scrollable = len(open_df) > _SCROLL_THRESHOLD
    table_wrapper_open = (
        '<div class="data-table__scroll-wrapper">' if scrollable else ""
    )
    table_wrapper_close = "</div>" if scrollable else ""

    table = f"""
{table_wrapper_open}
<table class="data-table">
  <thead>
    <tr>
      <th>Initiative</th>
      <th>Objective</th>
      <th>Signatures</th>
      <th>Countries Threshold</th>
    </tr>
  </thead>
  <tbody>
    {rows}
  </tbody>
</table>
{table_wrapper_close}"""

    return wrap_card(title + table)
