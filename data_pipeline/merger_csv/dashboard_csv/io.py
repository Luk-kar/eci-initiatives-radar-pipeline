"""
Dashboard Merger File I/O
-------------------------
CSV resolution, validation, and loading helpers for the dashboard merger.

Mirrors the structure of
``data_pipeline/merger_csv/responses_followup_legislation/io.py`` so the two
merger steps stay self-contained while sharing a familiar API.
"""

import csv
import logging
import re
from pathlib import Path

from data_pipeline.pipeline_shared.consts import FILE_ENCODING, FilePatterns

logger = logging.getLogger(__name__)


# ── Run-directory resolution ──────────────────────────────────────────────────
def find_latest_data_dir(data_dir: Path) -> Path:
    """Return the lexicographically latest timestamped run directory.

    Run directories follow the ``YYYY-MM-DD_HH-MM-SS`` pattern, which sorts
    chronologically. Unlike ``find_newest_scraped_data_dir`` from
    ``pipeline_shared``, this helper does **not** validate HTML content —
    the dashboard merger only reads CSV files produced by earlier steps.

    Args:
        data_dir: Top-level data directory (``data_pipeline/data``).

    Returns:
        Path to the newest matching run directory.

    Raises:
        FileNotFoundError: If no timestamped directories are found.
    """

    pattern = re.compile(FilePatterns.TIMESTAMP_DIR_PATTERN)
    candidates = sorted(
        p for p in data_dir.iterdir() if p.is_dir() and pattern.fullmatch(p.name)
    )

    if not candidates:
        raise FileNotFoundError(
            f"No timestamped run directories found under: {data_dir}"
        )

    latest = candidates[-1]
    logger.info("Resolved latest data directory: %s", latest)
    return latest


# ── CSV resolution / validation / loading ─────────────────────────────────────
def find_latest_csv(data_dir: Path, glob_pattern: str) -> Path:
    """Return the lexicographically latest CSV matching *glob_pattern* in *data_dir*.

    Args:
        data_dir:     Directory to search (typically a timestamped run dir).
        glob_pattern: Glob expression such as ``"eci_initiatives_[0-9]*.csv"``.

    Returns:
        Matching ``Path``.

    Raises:
        FileNotFoundError: If no files match.
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
    """Validate that *path* is a regular CSV file with at least one data row.

    Raises:
        FileNotFoundError: ``path`` does not exist or is not a regular file.
        ValueError:        ``path`` is empty or contains only a header row.
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
    """Load a CSV into memory using ``csv.DictReader``.

    Args:
        path: Source CSV path.

    Returns:
        List of dict rows, in source order.
    """
    logger.info("Loading CSV %s", path)

    with path.open(encoding=FILE_ENCODING, newline="") as fh:
        rows = list(csv.DictReader(fh))

    logger.debug("%d rows loaded from %s", len(rows), path.name)
    return rows


# ── Column filtering ──────────────────────────────────────────────────────────
def filter_columns(
    rows: list[dict[str, str]],
    keep: tuple[str, ...],
    *,
    source_label: str,
) -> list[dict[str, str]]:
    """Return *rows* narrowed to only the columns listed in *keep*.

    Missing values are coerced to empty strings so downstream consumers can
    rely on every row having every key.

    Args:
        rows:         Source rows.
        keep:         Columns to retain, in any order.
        source_label: Human-readable label for the CSV (used in error messages).

    Returns:
        New list of dict rows containing exactly *keep*.

    Raises:
        ValueError: If *rows* is non-empty and any column in *keep* is not
                    present in the source CSV header.
    """
    if not rows:
        return []

    header = set(rows[0].keys())

    missing = [col for col in keep if col not in header]

    if missing:
        raise ValueError(
            f"{source_label}: missing required column(s) {missing!r}; "
            f"got header={sorted(header)!r}"
        )

    filtered = [{col: (row.get(col) or "") for col in keep} for row in rows]

    logger.debug(
        "%s: kept %d/%d columns across %d row(s)",
        source_label,
        len(keep),
        len(header),
        len(filtered),
    )

    return filtered
