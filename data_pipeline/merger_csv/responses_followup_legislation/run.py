"""
Legislation Extraction Pipeline
Coordinates the full legislation extraction step from source rows to output CSV.
"""

import logging
from pathlib import Path

from .assemble import assemble_results
from .collect import collect_source_rows
from .write import write_output

logger = logging.getLogger(__name__)


def run(data_dir: Path) -> Path:
    """
    Execute the full legislation-extraction pipeline step.

    Steps
    -----
    1. Resolve the most recent responses and follow-up CSVs.
    2. Validate and load both CSVs.
    3. Validate cross-file registration-number consistency.
    4. Concatenate text fields and run regex extraction for each initiative.
    5. Write the output CSV and return its path.

    Args:
        data_dir: Timestamped run directory.

    Returns:
        Path to the written output CSV.
    """
    responses_rows, followup_rows = collect_source_rows(data_dir)
    results = assemble_results(responses_rows, followup_rows)

    logger.info("Regex extraction complete. %d initiative(s) processed.", len(results))

    return write_output(data_dir, results)