"""
Colors used on the page
"""

from typing import NamedTuple


class KpiColors(NamedTuple):
    total_initiatives: str = "#2A3F69"
    currently_open: str = "#1069c0"
    reached_signatures: str = "#557B2D"
    got_response: str = "#006064"
    led_to_legislation: str = "#6a1b9a"


kpi_colors = KpiColors()
