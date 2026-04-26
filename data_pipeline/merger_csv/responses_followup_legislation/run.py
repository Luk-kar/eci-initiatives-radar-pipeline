"""
Legislation Extraction Pipeline
Coordinates the full legislation extraction step from source rows to output CSV.
"""

import logging
from pathlib import Path

from .assemble import assemble_results
from .collect import collect_source_rows
from .session import setup
from .write import write_output

logger = logging.getLogger(__name__)


def run() -> Path:
    """
    Execute the full legislation-extraction pipeline step.

    Returns:
        Path to the written output CSV.
    """

    global logger

    data_dir, step_logger = setup()
    logger = step_logger

    logger.info("Starting legislation extraction in %s", data_dir)

    responses_rows, followup_rows = collect_source_rows(data_dir)
    logger.info(
        "Source collection complete. responses=%d, follow-up=%d",
        len(responses_rows),
        len(followup_rows),
    )

    results = assemble_results(responses_rows, followup_rows)
    logger.info("Analysis complete. %d initiative(s) processed", len(results))

    output_path = write_output(data_dir, results)
    logger.info("Done. Legislation output written to %s", output_path)

    return output_path
