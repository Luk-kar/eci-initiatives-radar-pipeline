import pandas as pd


def kpi_row_containers(df: pd.DataFrame) -> str:
    metrics = [
        {
            "label": "Total Initiatives:",
            "value": len(df),
            "color": "#1a237e",
            "icon": "📋",
        },
        {
            "label": "Currently Open:",
            "value": int((df["outcome"] == "Pending").sum()),
            "color": "#2e7d32",
            "icon": "🗳️",
        },
        {
            "label": "Reached 1M Signatures:",
            "value": int((df["signatures_numeric"] >= 1_000_000).sum()),
            "color": "#827717",
            "icon": "✅",
        },
        {
            "label": "Got EU Response:",
            "value": int(df["outcome"].notna().sum()),
            "color": "#006064",
            "icon": "📬",
        },
        {
            "label": "Led to Legislation:",
            "value": int((df["outcome"] == "Proposal").sum()),
            "color": "#6a1b9a",
            "icon": "⚖️",
        },
    ]

    cards = "\n".join(
        f"""      <div class="kpi-card">
        <span class="kpi-label">{m["icon"]} {m["label"]}</span>
        <span class="kpi-value" style="color:{m["color"]}">{m["value"]}</span>
      </div>"""
        for m in metrics
    )

    return f"""<div class="kpi-row">
{cards}
</div>"""
