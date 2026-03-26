"""
CSV operations for the Commission responses scraper.
"""

from typing import Dict, List

# Shared
from ...scraper_shared.files_utils import write_csv
from data_pipeline.pipeline_shared.consts import (
    FILE_ENCODING,
)  # noqa: F401 (re-exported via write_csv)

# Local
from ..consts import CSV_FIELDNAMES
from .._logger import logger


def write_responses_csv(file_path: str, response_data: List[Dict[str, str]]) -> None:
    """Write response data to CSV, normalizing registration numbers.

    Converts underscore format to slash format (2019_000007 → 2019/000007)
    to match the initiatives CSV format for downstream joins.

    Args:
        file_path: Full path to the output CSV file.
        response_data: List of response record dicts matching CSV_FIELDNAMES.
    """
    normalized = []

    for record in response_data:
        norm = record.copy()
        if "registration_number" in norm:
            norm["registration_number"] = norm["registration_number"].replace("_", "/")
        normalized.append(norm)

    write_csv(file_path, CSV_FIELDNAMES, normalized)
    logger.debug(f"CSV written: {file_path}")
