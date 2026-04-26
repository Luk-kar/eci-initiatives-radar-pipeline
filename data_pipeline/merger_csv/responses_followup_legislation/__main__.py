"""
ECI Follow-up Legislation Extractor
Runs the legislation extraction step for the latest available ECI response data.
"""

import logging
import sys

from data_pipeline.pipeline_shared.errors import RunDirectoryValidationError

from .run import run

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the legislation extraction command-line entry point."""
    try:
        output_path = run()  # setting logger logic is here

    except RunDirectoryValidationError as exc:
        logger.error("Failed to resolve run directory: %s", exc)
        sys.exit(1)

    except (FileNotFoundError, ValueError, OSError) as exc:
        logger.error("Pipeline step failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
