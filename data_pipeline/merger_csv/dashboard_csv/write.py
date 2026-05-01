"""
Dashboard Merger Output Writer
------------------------------
Writes the assembled ``DashboardRow`` objects to the final dashboard CSV.
"""

import csv
import logging
from datetime import datetime
from pathlib import Path

from data_pipeline.pipeline_shared.consts import (
    ECI_DASHBOARD_CSV_PATTERN,
    FILE_ENCODING,
    TIMESTAMP_FORMAT,
)

from .extractor import DashboardRow
from .session import OUTPUT_FIELDNAMES

logger = logging.getLogger(__name__)


def write_output(data_dir: Path, results: list[DashboardRow]) -> Path:
    """Write the merged dashboard CSV to the run directory.

    Args:
        data_dir: Run directory to write into.
        results:  Rows to serialise (already sorted upstream).

    Returns:
        Path to the written CSV.
    """
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    filename = ECI_DASHBOARD_CSV_PATTERN.format(timestamp=timestamp)
    output_path = data_dir / filename

    logger.info("Writing dashboard CSV %s", output_path)

    with output_path.open("w", encoding=FILE_ENCODING, newline="") as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_FIELDNAMES)
        writer.writeheader()

        for result in results:
            # Use Pydantic's native model_dump() instead of dataclasses.asdict()
            writer.writerow(result.model_dump())

    logger.info("Wrote %d row(s) to %s", len(results), output_path)
    return output_path
