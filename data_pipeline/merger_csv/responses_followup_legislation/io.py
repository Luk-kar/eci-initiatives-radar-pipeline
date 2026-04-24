"""
Legislation Extraction File I/O
Finds, validates, and loads source CSV files for the legislation pipeline step.
"""

import csv
import logging
from pathlib import Path

from data_pipeline.pipeline_shared.consts import FILE_ENCODING

logger = logging.getLogger(__name__)


def find_latest_csv(data_dir: Path, glob_pattern: str) -> Path:
    """
    Return the lexicographically latest CSV matching *glob_pattern* inside *data_dir*.

    Args:
        data_dir:      Timestamped run directory.
        glob_pattern:  Glob expression such as ``"eci_responses_[0-9]*.csv"``.

    Returns:
        Matching ``Path``.

    Raises:
        FileNotFoundError: if no files match.
    """
    matches = sorted(data_dir.glob(glob_pattern))

    if not matches:
        raise FileNotFoundError(
            f"No files matching {glob_pattern!r} found in directory: {data_dir}"
        )

    latest = matches[-1]
    logger.info("Resolved %s -> %s", glob_pattern, latest.name)
    return latest


def validate_csv_exists(path: Path) -> None:
    """
    Validate that *path* exists, is a file, and contains at least one data row.

    Args:
        path: CSV file to validate.

    Raises:
        FileNotFoundError: the path does not exist or is not a regular file.
        ValueError:        the CSV is empty or contains only a header row.
    """
    if not path.exists():
        raise FileNotFoundError(f"Required CSV does not exist: {path}")

    if not path.is_file():
        raise FileNotFoundError(f"Expected a regular file but found: {path}")

    with path.open(encoding=FILE_ENCODING, newline="") as fh:
        reader = csv.reader(fh)

        try:
            next(reader)
        except StopIteration as exc:
            raise ValueError(f"CSV file is completely empty: {path}") from exc

        try:
            next(reader)
        except StopIteration as exc:
            raise ValueError(f"CSV file contains no data rows: {path}") from exc


def load_csv(path: Path) -> list[dict[str, str]]:
    """
    Load a CSV into memory with ``csv.DictReader``.

    Args:
        path: Source CSV path.

    Returns:
        List of dict rows.
    """
    logger.info("Loading CSV %s", path)

    with path.open(encoding=FILE_ENCODING, newline="") as fh:
        rows = list(csv.DictReader(fh))

    logger.debug("%d rows loaded from %s", len(rows), path.name)
    return rows