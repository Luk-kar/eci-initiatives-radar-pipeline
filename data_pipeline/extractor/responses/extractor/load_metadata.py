"""
Load and validate CSV metadata against the collected HTML files.
"""

import csv
import logging
from pathlib import Path
from typing import Dict, Set

from data_pipeline.pipeline_shared.consts import FILE_ENCODING


logger = logging.getLogger(__name__)


def load_metadata(
    initiatives_csv: Path,
    html_files: Dict[str, Path],
) -> Dict[str, dict]:
    """
    Load initiatives CSV rows filtered to reg numbers found on disk,
    then assert every HTML file has a matching CSV record.

    Returns:
        Dict mapping registration_number → CSV row dict.

    Raises:
        FileNotFoundError: If any HTML file has no matching CSV record.
    """
    metadata = _load_responses_metadata(
        initiatives_csv, reg_numbers=set(html_files.keys())
    )
    logger.info("Matched %d CSV records to HTML files", len(metadata))

    unmatched = set(html_files.keys()) - set(metadata.keys())
    if unmatched:
        raise FileNotFoundError(
            f"{len(unmatched)} HTML files have no matching CSV record: {sorted(unmatched)}"
        )

    return metadata


def _load_responses_metadata(
    csv_path: Path,
    reg_numbers: Set[str],
) -> Dict[str, dict]:
    """
    Load the initiatives CSV filtered to the given set of reg numbers.

    Args:
        csv_path:    Path to the latest eci_initiatives_*.csv.
        reg_numbers: Only rows whose registration_number is in this set are kept.

    Returns:
        Dict mapping registration_number → row dict.
    """
    metadata: Dict[str, dict] = {}

    with open(csv_path, encoding=FILE_ENCODING) as f:
        for row in csv.DictReader(f):
            reg_num = row["registration_number"]
            if reg_num and reg_num in reg_numbers:
                metadata[reg_num] = row

    return metadata
