"""
Session-scoped fixtures for the initiatives end-to-end test suite.

Runs a deliberately limited live scrape against the EU server:
  - exactly 1 listing page (pagination mocked to stop early)
  - MAX_INITIATIVES_E2E individual initiative pages

Yields a ScrapeArtifacts dataclass with all resolved paths so that every
test in this package shares one scraping session and one browser instance.
After the session the timestamped data directory is removed automatically.
"""

# Standard library
import datetime
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

# Third-party
import pytest

# ── Tuning ─────────────────────────────────────────────────────────────────────
MAX_INITIATIVES_E2E = 2  # pages to hit on the EU server; keep small

# ── Patch targets ──────────────────────────────────────────────────────────────
_LISTINGS_FETCHER = "data_pipeline.scraper.initiatives.fetchers.listings.fetcher"


@dataclass
class ScrapeArtifacts:
    timestamp: str
    data_path: Path
    listings_path: Path
    pages_path: Path
    logs_path: Path


@pytest.fixture(scope="session")
def e2e_scrape(tmp_path_factory) -> ScrapeArtifacts:
    """Run a limited live scrape and yield resolved directory paths.

    Imports are deferred into the fixture body so that module-level side
    effects (log-file creation, timestamp freezing) only fire when the
    fixture is actually used, not at collection time.
    """

    # ── Deferred imports ──────────────────────────────────────────────────────
    from data_pipeline.scraper.initiatives.browser import initialize_browser
    from data_pipeline.scraper.initiatives.fetchers.listings import scrape_all_listings
    from data_pipeline.scraper.initiatives.fetchers.ecis import download_all_initiatives
    from data_pipeline.scraper.initiatives import data_parser

    from data_pipeline.scraper.initiatives.consts import (
        DATA_DIR_NAME,
        LISTINGS_DIR_NAME,
        PAGES_DIR_NAME,
        LOG_DIR_NAME,
        CSV_FIELDNAMES,
        CSV_FILENAME,
    )
    from data_pipeline.scraper.scraper_shared.consts import BASE_URL

    from data_pipeline.scraper.scraper_shared.fs_utils import (
        build_timestamped_run_dirs,
        ensure_dirs,
        write_csv,
    )

    # ── Build directories ─────────────────────────────────────────────────────
    tmp_root = tmp_path_factory.mktemp("eci_e2e")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_e2e"

    PIPELINE_DIR = str(tmp_root)  # Replacement to not trash the project

    dirs = build_timestamped_run_dirs(
        PIPELINE_DIR,
        DATA_DIR_NAME,
        timestamp,
        LISTINGS_DIR_NAME,
        PAGES_DIR_NAME,
        LOG_DIR_NAME,
    )

    list_dir = dirs[LISTINGS_DIR_NAME]
    pages_dir = dirs[PAGES_DIR_NAME]
    log_dir = dirs[LOG_DIR_NAME]
    ensure_dirs(list_dir, pages_dir, log_dir)

    # ── Mocks ─────────────────────────────────────────────────────────────────
    _original_parse = data_parser.parse_initiatives_list_data

    def _limited_parse(page_source: str, base_url: str) -> list:
        """Parse normally but truncate to MAX_INITIATIVES_E2E entries."""
        return _original_parse(page_source, base_url)[:MAX_INITIATIVES_E2E]

    def _stop_at_first_page(driver, current_page: int) -> bool:
        """Prevent pagination so only page 1 is scraped."""
        return False

    # ── Live scrape ───────────────────────────────────────────────────────────
    driver = initialize_browser()

    try:
        with (
            patch(
                f"{_LISTINGS_FETCHER}.parse_initiatives_list_data",
                side_effect=_limited_parse,
            ),
            patch(
                f"{_LISTINGS_FETCHER}.navigate_to_next_page",
                side_effect=_stop_at_first_page,
            ),
        ):
            initiative_data, _ = scrape_all_listings(driver, BASE_URL, list_dir)

        updated_data, _ = download_all_initiatives(driver, pages_dir, initiative_data)

    finally:
        driver.quit()

    csv_path = os.path.join(list_dir, CSV_FILENAME)
    write_csv(csv_path, CSV_FIELDNAMES, updated_data)

    # ── Yield artifacts ───────────────────────────────────────────────────────
    data_path = Path(PIPELINE_DIR) / DATA_DIR_NAME / timestamp

    artifacts = ScrapeArtifacts(
        timestamp=timestamp,
        data_path=data_path,
        listings_path=Path(list_dir),
        pages_path=Path(pages_dir),
        logs_path=Path(log_dir),
    )

    yield artifacts

    # No manual shutil.rmtree needed — pytest cleans tmp_path_factory automatically
