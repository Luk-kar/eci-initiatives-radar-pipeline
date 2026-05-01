"""
Legislation Extraction Output Writer
Writes structured legislation results to the final CSV output.
"""

import csv
import logging
from datetime import datetime
from pathlib import Path

from data_pipeline.pipeline_shared.consts import (
    ECI_RESPONSES_FOLLOWUP_LEGISLATION_PATTERN,
    FILE_ENCODING,
    TIMESTAMP_FORMAT,
)

from .extractor import LegislationResult
from .session import OUTPUT_FIELDNAMES

logger = logging.getLogger(__name__)


def write_output(data_dir: Path, results: list[LegislationResult]) -> Path:
    """
    Write the legislation extraction output CSV.

    Args:
        data_dir: Output directory.
        results: Extracted rows.

    Returns:
        Path to the written CSV.
    """

    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    filename = ECI_RESPONSES_FOLLOWUP_LEGISLATION_PATTERN.format(timestamp=timestamp)
    output_path = data_dir / filename

    logger.info("Writing output CSV %s", output_path)

    with output_path.open("w", encoding=FILE_ENCODING, newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_FIELDNAMES)
        writer.writeheader()

        for result in results:
            writer.writerow(
                {
                    "registration_number": result.registration_number,
                    "commission_answer": result.commission_answer,
                    "followup_events": result.followup_events,
                    "law_passed": result.law_passed,
                    "Is_Law_Passed": result.Is_Law_Passed,
                    "Rejected_Legislation": result.Rejected_Legislation,
                }
            )

    logger.info("Wrote %d row(s) to %s", len(results), output_path)
    return output_path
