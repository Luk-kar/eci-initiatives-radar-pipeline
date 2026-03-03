import pandas as pd

from page_creator.utils import wrap_card


_STATUS = "Collection Ongoing"
_TRUNCATE = 100
_SCROLL_THRESHOLD = 5
_COUNTRIES_THRESHOLD = 7


def _truncate(text: str, max_len: int = _TRUNCATE) -> str:
    if pd.isna(text):
        return ""
    s = str(text)
    return s if len(s) <= max_len else s[: max_len - 1] + "…"


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
        sigs = (
            f"{int(row['signatures_collected']):,}"
            if pd.notna(row["signatures_collected"])
            else "N/A"
        )
        threshold = (
            f"{int(row['signatures_threshold_met'])} / {_COUNTRIES_THRESHOLD}"
            if pd.notna(row["signatures_threshold_met"])
            else "N/A"
        )

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
