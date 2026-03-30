"""
Logger factory for the responses extractor module.
"""

import logging
from pathlib import Path

from data_pipeline.pipeline_shared.consts import (
    LOG_EXTRACTOR_RESPONSES_PATTERN,
    TIMESTAMP_FORMAT,
)
from data_pipeline.pipeline_shared.logger import (
    set_console_handler,
    set_file_handler,
    set_logger_and_its_level,
)


def setup_logger(log_dir_path: Path, timestamp) -> logging.Logger:
    """Create or retrieve the configured responses-extractor logger.

    The logger name is derived from ``LOG_EXTRACTOR_RESPONSES_PATTERN`` by
    stripping the ``_{timestamp}.log`` suffix, which keeps
    ``logging.getLogger`` idempotent — calling ``setup_logger`` a second time
    with the same pattern returns the same instance without adding duplicate
    handlers.

    Args:
        log_dir_path: Directory where the log file will be written.  Created
            automatically if it does not exist.
        timestamp: Timestamp used to resolve the log filename.  Accepts either
            a pre-formatted ``str`` or a ``datetime`` object — in the latter
            case it is formatted with ``TIMESTAMP_FORMAT`` before use.

    Returns:
        Configured ``logging.Logger`` instance with a DEBUG-level file handler
        and an INFO-level console handler attached.
    """
    if not isinstance(timestamp, str):
        timestamp = timestamp.strftime(TIMESTAMP_FORMAT)

    log_dir_path.mkdir(parents=True, exist_ok=True)

    logger = set_logger_and_its_level(LOG_EXTRACTOR_RESPONSES_PATTERN)

    if logger.handlers:
        return logger

    log_path = log_dir_path / LOG_EXTRACTOR_RESPONSES_PATTERN.format(
        timestamp=timestamp
    )

    logger.addHandler(set_file_handler(log_path))
    logger.addHandler(set_console_handler())

    return logger
