"""
Merge CSV metadata and parsed HTML fields into ECIFollowupRecord.
"""

import logging
from typing import Dict, List

from ..model import ECIFollowupRecord
from .copy_fields.metadata import extract_metadata


logger = logging.getLogger(__name__)


def build_records(
    metadata: Dict[str, dict],
    parsed_data: Dict[str, dict],
) -> List[ECIFollowupRecord]:
    """
    Merge loaded CSV metadata with parsed HTML fields into ECIFollowupRecord.

    Args:
        metadata:    Raw CSV row dicts keyed by registration_number.
        parsed_data: HTML-extracted field dicts keyed by registration_number.

    Returns:
        List of fully assembled ECIFollowupRecord.
    """
    records: List[ECIFollowupRecord] = []

    for reg_number, parsed in parsed_data.items():
        csv_row = metadata[reg_number]
        relevant_metadata = extract_metadata(csv_row)
        records.append(ECIFollowupRecord(**relevant_metadata.model_dump(), **parsed))

    return records
