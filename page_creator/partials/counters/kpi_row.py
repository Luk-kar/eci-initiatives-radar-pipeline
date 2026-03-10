"""Renders the KPI summary strip — a row of clickable headline metric cards."""

# Third party
import pandas as pd


def generate_kpi_row(df: pd.DataFrame) -> str:
    """Return an HTML ``kpi-row`` div containing one clickable card per headline metric.

    Each card displays an icon, label, and computed value derived from ``df``,
    and scrolls the page to the corresponding list section when clicked.

    Args:
        df: The full ECI initiatives DataFrame. Must contain ``current_status``
            and ``signatures_collected`` columns.

    Returns:
        An HTML string containing the ``kpi-row`` div with all metric cards.
    """

    metrics = [
        {
            "label": "Total Initiatives:",
            "value": len(df),
            "color": "#333",
            "icon": "📋",
            "target_id": "total-initiatives-list-slot",
        },
        {
            "label": "Currently Open:",
            "value": int((df["current_status"] == "Collection Ongoing").sum()),
            "color": "#1069c0",
            "icon": "🗳️",
            "target_id": "currently-open-list-slot",
        },
        {
            "label": "Reached 1M Signatures:",
            "value": int((df["signatures_collected"] >= 1_000_000).sum()),
            "color": "#557B2D",
            "icon": "✅",
            "target_id": "reached-signatures-list-slot",
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
            "target_id": "got-response-list-slot",
        },
        {
            "label": "Led to Legislation:",
            "value": int((df["current_status"] == "Law Passed").sum()),
            "color": "#6a1b9a",
            "icon": "⚖️",
            "target_id": "led-to-legislation-list-slot",
        },
    ]

    cards = "\n".join(
        f"""      <div class="kpi-card"
           role="button"
           tabindex="0"
           title="Scroll to {m['label'].rstrip(':')} list"
           style="cursor:pointer;"
           onclick="scrollToSection('{m['target_id']}')"
           onkeydown="if(event.key==='Enter'||event.key===' ')scrollToSection('{m['target_id']}')">
        <span class="kpi-label">{m["icon"]} {m["label"]}</span>
        <span class="kpi-value" style="color:{m["color"]}">{m["value"]}</span>
      </div>"""
        for m in metrics
    )

    return f"""<div class="kpi-row">
{cards}
</div>"""
