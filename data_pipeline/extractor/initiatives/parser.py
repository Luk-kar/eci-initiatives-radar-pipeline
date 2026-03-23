"""
HTML parser for individual ECI initiative pages.

Responsible for extracting structured data from a single initiative HTML file.
Implementation is pending.
"""

from typing import List
from pathlib import Path


def parse_initiative_page(html_file: Path, csv_columns: List[str]) -> dict:
    """
    Parse a single ECI initiative HTML file.

    Args:
        html_file: Path to the initiative HTML file
                   (e.g. ``initiatives/2023/2023_000009_en.html``).

    Returns:
        Dictionary containing the following keys:

        - ``registration_number``
        - ``title``
        - ``objective``
        - ``annex``
        - ``current_status``
        - ``url``
        - ``timeline_registered``
        - ``timeline_collection_start_date``
        - ``timeline_collection_closed``
        - ``timeline_response_commission_date``
        - ``timeline``
        - ``funding_total``
        - ``signatures_collected``
        - ``signatures_collected_by_country``
        - ``signatures_threshold_met``
        - ``response_commission_url``
    """
    raise NotImplementedError
