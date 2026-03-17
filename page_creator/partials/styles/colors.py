"""
Colors used on the page
"""

from typing import NamedTuple


class KpiColors(NamedTuple):
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


kpi_colors = KpiColors()
