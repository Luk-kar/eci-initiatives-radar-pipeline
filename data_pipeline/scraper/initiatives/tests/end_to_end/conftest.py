"""
Session-scoped fixtures for the initiatives end-to-end test suite.

Runs a deliberately limited live scrape against the EU server:
  - exactly 1 listing page  (pagination mocked to stop early)
  - MAX_INITIATIVES_E2E individual initiative pages

LOG_DIR and PIPELINE_DIR are already redirected to a temp directory by
the autouse fixture in data_pipeline/scraper/initiatives/conftest.py.
This fixture only handles the e2e-specific data directories and scraping mocks.
"""

# Standard library
import datetime
import os
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

# Third-party
import pytest

# ── Tuning ─────────────────────────────────────────────────────────────────────
MAX_INITIATIVES_E2E = 2

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
    """Run a limited live scrape; all output lands in a pytest temp directory."""

    tmp_root = tmp_path_factory.mktemp("eci_e2e")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_e2e"

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

    # ── Build run directories under tmp ───────────────────────────────────────
    dirs = build_timestamped_run_dirs(
        str(tmp_root),
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

    # ── Scraping mocks ────────────────────────────────────────────────────────
    _original_parse = data_parser.parse_initiatives_list_data

    def _limited_parse(page_source: str, base_url: str) -> list:
        return _original_parse(page_source, base_url)[:MAX_INITIATIVES_E2E]

    def _stop_at_first_page(driver, current_page: int) -> bool:
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

    write_csv(os.path.join(list_dir, CSV_FILENAME), CSV_FIELDNAMES, updated_data)

    # ── Yield ─────────────────────────────────────────────────────────────────
    yield ScrapeArtifacts(
        timestamp=timestamp,
        data_path=tmp_root / DATA_DIR_NAME / timestamp,
        listings_path=Path(list_dir),
        pages_path=Path(pages_dir),
        logs_path=Path(log_dir),
    )
