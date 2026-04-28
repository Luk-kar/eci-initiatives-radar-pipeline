"""
ECI Dashboard CSV Merger
Runs the dashboard CSV merge step against the latest available run directory.
"""

import logging
import sys

from data_pipeline.pipeline_shared.errors import RunDirectoryValidationError

from .run import run

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the dashboard CSV merger command-line entry point."""
    try:
        run()
    except RunDirectoryValidationError as exc:
        logger.error("Failed to resolve run directory: %s", exc)
        sys.exit(1)
    except (FileNotFoundError, ValueError, OSError) as exc:
        logger.error("Pipeline step failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
