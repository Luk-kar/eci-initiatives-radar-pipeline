"""
CSV writer — serializes ECIResponseRecords to the output CSV file.
"""

import csv
import logging
from pathlib import Path
from typing import List

from ..model import ECIResponseRecord
from data_pipeline.pipeline_shared.consts import FILE_ENCODING


logger = logging.getLogger(__name__)


def write_csv(records: List[ECIResponseRecord], output_csv: Path) -> None:
    """
    Serialize records and write to CSV.

    Raises:
        ValueError: If records list is empty.
    """
    if not records:
        raise ValueError("No records to write.")

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with open(output_csv, "w", encoding=FILE_ENCODING, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ECIResponseRecord.model_fields))
        writer.writeheader()

        for record in records:
            writer.writerow(record.model_dump())

    logger.info("Wrote %d rows to %s", len(records), output_csv)
