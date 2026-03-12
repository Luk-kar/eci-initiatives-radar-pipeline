"""Renders the KPI summary strip — a row of clickable headline metric cards."""

# Third party
import pandas as pd

# Local
from page_creator.partials.styles.colors import kpi_colors as colors


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
            "color": colors.total_initiatives,
            "icon": "📋",
            "target_id": "total-initiatives-list-slot",
        },
        {
            "label": "Currently Open:",
            "value": int((df["current_status"] == "Collection Ongoing").sum()),
            "color": colors.currently_open,
            "icon": "🗳️",
            "target_id": "currently-open-list-slot",
        },
        {
            "label": "Reached 1M Signatures:",
            "value": int((df["signatures_collected"] >= 1_000_000).sum()),
            "color": colors.reached_signatures,
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
            "color": colors.got_response,
            "icon": "📬",
            "target_id": "got-response-list-slot",
        },
        {
            "label": "Led to Legislation:",
            "value": int((df["current_status"] == "Law Passed").sum()),
            "color": colors.led_to_legislation,
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
