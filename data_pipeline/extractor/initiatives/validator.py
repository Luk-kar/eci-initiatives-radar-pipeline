"""
Pre-extraction validator for the ECI initiatives run directory.

Checks that the newest data run contains:
- a valid initiatives/ directory with year subdirectories
- at least one HTML file per year directory, validated as real HTML
- a logs/ directory
"""

import logging
from pathlib import Path

from data_pipeline.consts import (
    INITIATIVES_DIR_NAME,
    LOG_DIR_NAME,
    INITIATIVE_PAGE_FILENAME_PATTERN,
)

logger = logging.getLogger(__name__)

# Minimum bytes to consider an HTML file non-trivially populated
_MIN_HTML_BYTES = 256

# Tokens that must appear in a valid ECI initiative HTML page
_REQUIRED_HTML_TOKENS = ("<html", "citizens-initiative.europa.eu")


class RunDirectoryValidationError(Exception):
    """Raised when the run directory fails structural or content validation."""


def find_newest_run_dir(data_dir: Path) -> Path:
    """
    Return the most recent timestamped run directory under *data_dir*.

    Directories are expected to follow the ``YYYY-MM-DD_HH-MM-SS`` pattern,
    which sorts lexicographically in chronological order.

    Args:
        data_dir: Top-level data directory (e.g. ``data_pipeline/data``).

    Returns:
        Path to the newest run directory.

    Raises:
        RunDirectoryValidationError: If no run directories are found.
    """
    candidates = [p for p in data_dir.iterdir() if p.is_dir()]
    if not candidates:
        raise RunDirectoryValidationError(f"No run directories found under: {data_dir}")

    newest = max(candidates, key=lambda p: p.name)
    logger.info("Newest run directory: %s", newest)
    return newest


def validate_run_dir(run_dir: Path) -> None:
    """
    Validate that *run_dir* has the expected structure and valid HTML content.

    Checks performed:
    1. ``initiatives/`` subdirectory exists.
    2. At least one year directory (4-digit name) exists inside ``initiatives/``.
    3. Each year directory contains at least one HTML file.
    4. Every HTML file passes basic content validation.
    5. ``logs/`` subdirectory exists.

    Args:
        run_dir: A timestamped run directory, e.g.
                 ``data_pipeline/data/2026-03-22_15-51-04``.

    Raises:
        RunDirectoryValidationError: On the first failed check encountered.
    """
    _validate_logs_dir(run_dir)
    initiatives_dir = _validate_initiatives_dir(run_dir)
    year_dirs = _validate_year_dirs(initiatives_dir)
    for year_dir in year_dirs:
        html_files = _validate_html_files_present(year_dir)
        for html_file in html_files:
            _validate_html_content(html_file)

    logger.info("Run directory validated successfully: %s", run_dir)


# ── Private helpers ────────────────────────────────────────────────────────────


def _validate_logs_dir(run_dir: Path) -> Path:
    logs_dir = run_dir / LOG_DIR_NAME
    if not logs_dir.exists():
        raise RunDirectoryValidationError(f"Missing logs directory: {logs_dir}")
    logger.debug("logs/ directory present: %s", logs_dir)
    return logs_dir


def _validate_initiatives_dir(run_dir: Path) -> Path:
    initiatives_dir = run_dir / INITIATIVES_DIR_NAME
    if not initiatives_dir.is_dir():
        raise RunDirectoryValidationError(
            f"Missing initiatives directory: {initiatives_dir}"
        )
    logger.debug("initiatives/ directory present: %s", initiatives_dir)
    return initiatives_dir


def _validate_year_dirs(initiatives_dir: Path) -> list[Path]:
    year_dirs = [
        p
        for p in sorted(initiatives_dir.iterdir())
        if p.is_dir() and p.name.isdigit() and len(p.name) == 4
    ]
    if not year_dirs:
        raise RunDirectoryValidationError(
            f"No year subdirectories found in: {initiatives_dir}"
        )
    logger.debug(
        "Found %d year director(ies): %s",
        len(year_dirs),
        [d.name for d in year_dirs],
    )
    return year_dirs


def _validate_html_files_present(year_dir: Path) -> list[Path]:
    html_files = sorted(year_dir.glob("*.html"))
    if not html_files:
        raise RunDirectoryValidationError(
            f"No HTML files found in year directory: {year_dir}"
        )
    logger.debug("Year %s — %d HTML file(s) found", year_dir.name, len(html_files))
    return html_files


def _validate_html_content(html_file: Path) -> None:
    """
    Check that *html_file* is non-trivially populated and contains
    the expected ECI HTML tokens.

    Raises:
        RunDirectoryValidationError: If the file is too small or lacks
                                     required content markers.
    """
    size = html_file.stat().st_size
    if size < _MIN_HTML_BYTES:
        raise RunDirectoryValidationError(
            f"HTML file too small ({size} bytes), likely truncated: {html_file}"
        )

    try:
        content = html_file.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise RunDirectoryValidationError(
            f"Could not read HTML file: {html_file}"
        ) from exc

    content_lower = content.lower()
    for token in _REQUIRED_HTML_TOKENS:
        if token.lower() not in content_lower:
            raise RunDirectoryValidationError(
                f"HTML file missing expected token {token!r}: {html_file}"
            )

    logger.debug("HTML validated: %s", html_file.name)
