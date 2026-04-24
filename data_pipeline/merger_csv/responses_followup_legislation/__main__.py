"""
ECI Follow-up Legislation Extractor
Runs the legislation extraction step for the latest available ECI response data.
"""

import logging
import sys

from data_pipeline.pipeline_shared.consts import (
    DATA_DIR,
    HTML_DOMAIN_EC_FOLLOWUP,
    LOG_DIR_NAME,
    LOG_LEGISLATION_PATTERN,
    RESPONSES_FOLLOWUP_DIR_NAME,
)
from data_pipeline.pipeline_shared.errors import RunDirectoryValidationError
from data_pipeline.pipeline_shared.locate_run_dir import find_newest_scraped_data_dir
from data_pipeline.pipeline_shared.logger import get_logger

from .run import run

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Run the legislation extraction command-line entry point.
    """

    try:
        data_dir = find_newest_scraped_data_dir(
            DATA_DIR,
            RESPONSES_FOLLOWUP_DIR_NAME,
            HTML_DOMAIN_EC_FOLLOWUP,
        )

    except RunDirectoryValidationError as exc:

        logging.getLogger(__name__).error("Failed to resolve run directory: %s", exc)
        sys.exit(1)

    get_logger(data_dir / LOG_DIR_NAME, LOG_LEGISLATION_PATTERN)

    try:
        output_path = run(data_dir)
        logger.info("[eci-extract-legislation] Done -> %s", output_path)

    except (FileNotFoundError, ValueError, OSError) as exc:

        logger.error("Pipeline step failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()