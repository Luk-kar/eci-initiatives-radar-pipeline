import pandas as pd


def generate_kpi_row(df: pd.DataFrame) -> str:
    metrics = [
        {
            "label": "Total Initiatives:",
            "value": len(df),
            "color": "#333",
            "icon": "📋",
        },
        {
            "label": "Currently Open:",
            "value": int((df["current_status"] == "Collection Ongoing").sum()),
            "color": "#1069c0",
            "icon": "🗳️",
        },
        {
            "label": "Reached 1M Signatures:",
            "value": int((df["signatures_collected"] >= 1_000_000).sum()),
            "color": "#557B2D",
            "icon": "✅",
        },
        {
            "label": "Got EU Response:",
            "value": int(
                df["current_status"]
                .isin(["Commission Engaged", "Law Passed", "Rejected Legislation"])
                .sum()
            ),
            "color": "#006064",
            "icon": "📬",
        },
        {
            "label": "Led to Legislation:",
            "value": int((df["current_status"] == "Law Passed").sum()),
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
