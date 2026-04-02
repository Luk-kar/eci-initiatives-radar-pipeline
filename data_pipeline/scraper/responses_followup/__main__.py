"""
Main entry point for the Commission responses follow-up scraper.

Reads follow-up website URLs from the ``followup_additional_website`` column
of the latest ``eci_responses_*.csv`` produced by the extractor, downloads
each page, and writes a summary CSV.
"""

import csv
import datetime
import os
from pathlib import Path
from typing import List, Tuple

from .consts import (
    LOG_DIR_NAME,
    RESPONSES_DIR_NAME,
    CSV_FILENAME,
    RESPONSES_CSV_GLOB,
    FOLLOWUP_URL_COLUMN,
    INITIATIVES_DIR_NAME,
)
from .log_messages import LOG_MESSAGES
from .fetchers.followup import download_all_responses
from .browser import initialize_browser
from .file_operations.csv import write_responses_csv
from .statistics import display_completion_summary
from ._logger import logger

from ..scraper_shared.files_utils import ensure_dirs

from data_pipeline.pipeline_shared.consts import (
    LOG_SCRAPER_RESPONSES_FOLLOWUP_PATTERN,
    DATA_DIR,
    FILE_ENCODING,
)
from data_pipeline.pipeline_shared.logger import get_logger
from data_pipeline.pipeline_shared.errors import RunDirectoryValidationError
from data_pipeline.pipeline_shared.locate_run_dir import find_newest_scraped_data_dir


def scrape_commission_responses() -> str:
    """Scrape Commission follow-up pages listed in the latest responses CSV.

    Finds the newest timestamped run directory that contains an
    ``eci_responses_*.csv``, reads the ``followup_additional_website`` column,
    downloads each page, and writes a summary CSV.

    Returns:
        Timestamp string of when scraping began.

    Raises:
        RunDirectoryValidationError: If no run dir with a responses CSV is found.
    """
    run_dir = _resolve_run_data_dir()
    csv_path = _resolve_response_csv(run_dir)
    _setup_file_logging(os.path.join(run_dir, LOG_DIR_NAME))

    start_scraping = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logger.info(LOG_MESSAGES["scraping_start"].format(timestamp=run_dir))

    response_links = _read_followup_links_from_csv(csv_path)
    if not response_links:
        return start_scraping

    responses_dir = _setup_responses_dir(run_dir)

    output_csv_path = os.path.join(responses_dir, CSV_FILENAME)
    _write_initial_csv(output_csv_path, response_links)

    updated_data, failed_urls = _run_downloads(responses_dir, response_links)

    _finalise_csv(output_csv_path, updated_data)

    display_completion_summary(
        start_scraping, response_links, failed_urls, len(updated_data), responses_dir
    )

    return start_scraping


# ── Step functions ─────────────────────────────────────────────────────────────


def _resolve_run_data_dir() -> Path:
    """Locate the newest valid timestamped run directory.

    Delegates to ``find_newest_scraped_data_dir``, which validates that
    the directory contains an ``initiatives/`` subdirectory with HTML files
    and a ``logs/`` directory.

    Returns:
        Path to the newest valid run directory.

    Raises:
        RunDirectoryValidationError: If no valid run directory is found.
    """

    try:
        return find_newest_scraped_data_dir(DATA_DIR, INITIATIVES_DIR_NAME)
    except RunDirectoryValidationError:
        logger.error(
            "No valid initiatives run directory found under: %s — "
            "run the initiatives scraper first.",
            DATA_DIR,
        )
        raise


def _resolve_response_csv(run_dir: Path) -> Path:
    """Return the newest ``eci_responses_*.csv`` inside *run_dir*.

    Mirrors the candidate-selection logic of ``find_newest_scraped_data_dir``:
    collect all matches, raise immediately if there are none, then pick the
    newest by filename (timestamps sort lexicographically).

    Args:
        run_dir: The validated run directory returned by ``_resolve_run_data_dir``.

    Returns:
        Path to the newest matching CSV file.

    Raises:
        RunDirectoryValidationError: If no ``eci_responses_*.csv`` exists in
                                     *run_dir*.
    """
    candidates = sorted(run_dir.glob(RESPONSES_CSV_GLOB))

    if not candidates:
        raise RunDirectoryValidationError(
            f"No '{RESPONSES_CSV_GLOB}' found in run directory: {run_dir} — "
            "run the extractor first."
        )

    newest = max(candidates, key=lambda p: p.name)
    logger.info("Using responses CSV: %s", newest)

    return newest


def _read_followup_links_from_csv(csv_path: str) -> list[dict]:
    """Read follow-up URLs and metadata from the responses CSV.

    Reads ``followup_additional_website`` as the scrape target URL.
    Derives ``year`` and ``reg_number`` from ``registration_number``
    (slash-separated, e.g. ``2019/000007``).  Rows with an empty URL
    or an unparseable registration number are skipped with a warning.

    Args:
        csv_path: Path to the ``eci_responses_*.csv`` file.

    Returns:
        List of dicts with keys ``url``, ``year``, ``reg_number``, ``title``,
        ``datetime`` — matching the shape expected by the fetcher.
    """
    links: list[dict] = []

    try:
        with open(csv_path, encoding=FILE_ENCODING, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get(FOLLOWUP_URL_COLUMN, "").strip()
                if not url:
                    continue

                reg = row.get("registration_number", "").strip()
                # Normalise both underscore and slash separators.
                parts = reg.replace("_", "/").split("/")
                if len(parts) != 2 or not parts[0].isdigit():
                    logger.warning(
                        "Skipping row — cannot parse registration_number %r", reg
                    )
                    continue

                year, reg_number = parts
                links.append(
                    {
                        "url": url,
                        "year": year,
                        "reg_number": reg_number,
                        "title": row.get("title", "").strip(),
                        "datetime": "",
                    }
                )

    except OSError as exc:
        logger.error("Cannot read responses CSV %s: %s", csv_path, exc)
        return []

    if not links:
        logger.warning(LOG_MESSAGES["no_links_found"])
    else:
        logger.info(LOG_MESSAGES["links_found"].format(count=len(links)))

    return links


def _setup_responses_dir(run_dir: str) -> str:
    """Create and return the responses output directory.

    Args:
        run_dir: Root of the current scraping run.
    """
    responses_dir = os.path.join(run_dir, RESPONSES_DIR_NAME)
    ensure_dirs(responses_dir)
    return responses_dir


def _run_downloads(
    responses_dir: str,
    response_links: list,
) -> Tuple[list, list]:
    """Initialise a browser, download all follow-up pages, and close the browser.

    Args:
        responses_dir: Base directory for saving HTML files.
        response_links: List of dicts with ``url``, ``year``, ``reg_number``,
                        ``title``.

    Returns:
        Tuple of (updated_data, failed_urls).
    """
    driver = initialize_browser()

    try:
        return download_all_responses(driver, responses_dir, response_links)
    finally:
        driver.quit()
        logger.info(LOG_MESSAGES["browser_closed"])


def _finalise_csv(csv_path: str, updated_data: list) -> None:
    """Overwrite the CSV with download timestamps from a completed run.

    Args:
        csv_path: Path to the output CSV file.
        updated_data: List of response dicts including populated datetimes.
    """
    write_responses_csv(csv_path, updated_data)
    logger.info(LOG_MESSAGES["csv_timestamps_updated"].format(path=csv_path))


# ── Internal helpers ───────────────────────────────────────────────────────────


def _setup_file_logging(log_dir: str) -> None:
    """Attach file and console handlers via the shared logger factory."""
    get_logger(Path(log_dir), LOG_SCRAPER_RESPONSES_FOLLOWUP_PATTERN)


def _write_initial_csv(csv_path: str, response_links: List[dict]) -> None:
    """Write initial CSV with empty datetimes as a pre-download checkpoint."""
    write_responses_csv(
        csv_path,
        [
            {
                "url_response_followup": link["url"],
                "registration_number": f"{link['year']}_{link['reg_number']}",
                "title": link["title"],
                "datetime": "",
            }
            for link in response_links
        ],
    )
    logger.info(f"Initial CSV created: {csv_path}")


if __name__ == "__main__":
    scrape_commission_responses()
