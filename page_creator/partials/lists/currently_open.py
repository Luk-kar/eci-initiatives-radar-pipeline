import pandas as pd

from page_creator.utils import wrap_card

_STATUS = "Collection Ongoing"
_TRUNCATE = 120


def _truncate(text: str, max_len: int = _TRUNCATE) -> str:
    if pd.isna(text):
        return ""
    return str(text) if len(str(text)) <= max_len else str(text)[: max_len - 1] + "…"


def _render_item(row: pd.Series) -> str:
    sigs = (
        f"{int(row['signatures_collected']):,}"
        if pd.notna(row["signatures_collected"])
        else "N/A"
    )
    threshold = (
        int(row["signatures_threshold_met"])
        if pd.notna(row["signatures_threshold_met"])
        else 0
    )
    objective = _truncate(row.get("objective", ""))
    url = row.get("url", "#") or "#"

    return f"""
<div class="list-item">
  <div class="list-item__header">
    <a class="list-item__title" href="{url}" target="_blank" rel="noopener noreferrer">
      {row['title']}
    </a>
    <span class="list-item__badge list-item__badge--ongoing">Collection Ongoing</span>
  </div>
  <p class="list-item__objective">{objective}</p>
  <div class="list-item__meta">
    <span>✍️ <strong>{sigs}</strong> signatures</span>
    <span>🇪🇺 <strong>{threshold}</strong> / 27 countries</span>
  </div>
</div>
"""


def generate_currently_open(df: pd.DataFrame) -> str:
    open_df = (
        df[df["current_status"] == _STATUS]
        .sort_values("signatures_collected", ascending=False)
        .reset_index(drop=True)
    )

    if open_df.empty:
        body = '<p class="list-empty">No initiatives currently open for signature collection.</p>'
    else:
        items = "".join(_render_item(row) for _, row in open_df.iterrows())
        body = f'<div class="list-items">{items}</div>'

    header = (
        f'<h3 class="card__title">'
        f"📋 Currently Open for Signatures"
        f'<span class="card__count">{len(open_df)}</span>'
        f"</h3>"
    )

    return wrap_card(header + body)
