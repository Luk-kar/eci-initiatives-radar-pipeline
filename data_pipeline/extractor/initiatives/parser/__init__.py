"""
HTML parser for individual ECI initiative pages.
"""

import dataclasses
import logging
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup

from data_pipeline.pipeline_shared.consts import FILE_ENCODING

from ..model import ECIInitiativeDetailsRecord
from .fields import (
    construct_url,
    extract_annex,
    extract_current_status,
    extract_funding_by,
    extract_funding_total,
    extract_objective,
    extract_registration_number,
    extract_response_commission_url,
    extract_signatures_by_country,
    extract_signatures_collected,
    extract_signatures_threshold_met,
    extract_timeline_data,
    extract_title,
)


class ECIHTMLParser:
    """Parser for ECI initiative HTML pages.

    Implements ``HTMLParserProtocol`` — exposes ``csv_columns`` and ``parse``
    so it can be passed directly to ``extract_html_to_csv``.

    Column schema is derived dynamically from ``ECIInitiativeDetailsRecord``
    field names, staying in sync with the model automatically.
    """

    csv_columns: list[str] = [
        f.name for f in dataclasses.fields(ECIInitiativeDetailsRecord)
    ]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def parse(self, html_file: Path) -> dict:
        """
        Parse a single ECI initiative HTML file.

        Args:
            html_file:   Path to the initiative HTML file
                         (e.g. ``initiatives/2023/2023_000009_en.html``).
            csv_columns: Ordered list of column names used to filter the
                         returned dictionary to only the expected CSV fields.

        Returns:
            Dictionary whose keys match ``csv_columns``.

        Raises:
            ValueError: If parsing fails for any reason; the original
                        exception is chained via ``__cause__``.
        """
        try:
            with open(html_file, "r", encoding=FILE_ENCODING) as f:
                soup = BeautifulSoup(f.read(), "html.parser")

            reg_number = extract_registration_number(html_file.name)
            timeline_data = extract_timeline_data(soup)
            title = extract_title(soup)
            url = construct_url(reg_number)

            initiative_data = ECIInitiativeDetailsRecord(
                registration_number=reg_number,
                title=title,
                objective=extract_objective(soup),
                annex=extract_annex(soup),
                current_status=extract_current_status(soup),
                url=url,
                timeline_registered=timeline_data.get("timeline_registered"),
                timeline_collection_start_date=timeline_data.get(
                    "timeline_collection_start_date"
                ),
                timeline_collection_closed=timeline_data.get(
                    "timeline_collection_closed"
                ),
                timeline_verification_start=timeline_data.get(
                    "timeline_verification_start"
                ),
                timeline_verification_end=timeline_data.get(
                    "timeline_verification_end"
                ),
                timeline_response_commission_date=timeline_data.get(
                    "timeline_response_commission_date"
                ),
                timeline=timeline_data.get("timeline"),
                funding_total=extract_funding_total(soup),
                funding_by=extract_funding_by(soup, html_file, title, url),
                signatures_collected=extract_signatures_collected(soup),
                signatures_collected_by_country=extract_signatures_by_country(
                    soup, html_file, title, url
                ),
                signatures_threshold_met=extract_signatures_threshold_met(soup),
                response_commission_url=extract_response_commission_url(soup),
            )

            self.logger.info("Successfully parsed %s", html_file.name)
            return dataclasses.asdict(initiative_data)

        except Exception as exc:
            raise ValueError(f"Error parsing {html_file}") from exc
