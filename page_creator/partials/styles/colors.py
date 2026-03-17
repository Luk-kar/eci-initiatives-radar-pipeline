"""Single source of truth for all colours used across page_creator/partials."""

from typing import NamedTuple


class KpiColors(NamedTuple):
    # ── KPI counters & list headers ───────────────────────────────────────
    total_initiatives: str = "#2A3F69"
    currently_open: str = "#3779BA"
    reached_signatures: str = "#527445"
    got_response: str = "#006064"
    led_to_legislation: str = "#3CA371"
    awaiting_response: str = "#9E9E9E"
    collection_unsuccessful: str = "#8B1111"
    commission_engaged: str = "#9CCC65"
    rejected_legislation: str = "#F44336"
    withdrawn: str = "#4B4B4B"

    # ── Shared chart decorations ──────────────────────────────────────────
    threshold_line: str = "#3AB23F"  # 1M signature dashed line
    map_text_outline: str = "#4d297f"  # choropleth country label shadow
    default_status: str = "#757575"  # fallback for unknown statuses


kpi_colors = KpiColors()


# ── Status → colour mapping (used by chart partials) ─────────────────────────
#
# Derived directly from kpi_colors so chart slices, KPI cards, and list
# headers always stay in sync. Add a new status here AND in KpiColors.
STATUS_COLORS: dict[str, str] = {
    "Law Passed": kpi_colors.led_to_legislation,
    "Commission Engaged": kpi_colors.commission_engaged,
    "Rejected Legislation": kpi_colors.rejected_legislation,
    "Awaiting Response": kpi_colors.awaiting_response,
    "Collection Ongoing": kpi_colors.currently_open,
    "Collection Unsuccessful": kpi_colors.collection_unsuccessful,
    "Withdrawn": kpi_colors.withdrawn,
}
