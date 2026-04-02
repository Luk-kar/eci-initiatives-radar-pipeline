"""
HTML parser for individual ECI initiative response pages.
"""

import logging
from pathlib import Path

from bs4 import BeautifulSoup

from data_pipeline.pipeline_shared.consts import FILE_ENCODING

from .model import ECIResponseParseHTMLRecord
from .fields import (
    extract_commission_answer,
    extract_followup_additional_website,
    extract_followup_events,
)


logger = logging.getLogger(__name__)

CSV_COLUMNS: list[str] = list(ECIResponseParseHTMLRecord.model_fields)


def parse_HTML(html_file: Path, registration_number: str) -> dict:
    """
    Parse a single ECI response HTML file.

    Args:
        html_file:            Path to the response HTML file
                              (e.g. ``responses/2023/2023_000009_en.html``).
        registration_number:  Initiative registration number used for logging
                              and extractor context.

    Returns:
        Dictionary whose keys match ``CSV_COLUMNS``.

    Raises:
        ValueError: If parsing fails for any reason; the original
                    exception is chained via ``__cause__``.
    """
    # try:
    with open(html_file, "r", encoding=FILE_ENCODING) as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    record = ECIResponseParseHTMLRecord(
        commission_answer_text=extract_commission_answer(soup, registration_number),
        followup_additional_website=extract_followup_additional_website(
            soup, registration_number
        ),
        followup_events=extract_followup_events(soup, registration_number),
    )

    logger.info("Successfully parsed %s", html_file.name)
    return record.model_dump()

    # except Exception as exc:
    #     raise ValueError(f"Error parsing {html_file}") from exc
