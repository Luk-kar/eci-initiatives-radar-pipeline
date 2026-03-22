"""
Session-scoped fixtures for the initiatives end-to-end test suite.

Runs a deliberately limited live scrape against the EU server:
  - exactly 1 listing page  (pagination mocked to stop early)
  - MAX_INITIATIVES_E2E individual initiative pages

All filesystem output — scraped HTML, CSV, and log files — is redirected
to a pytest-managed temp directory by patching the two path constants that
drive directory creation before any initiative module is imported.
pytest deletes the temp tree automatically after the session ends.
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
_INITIATIVES_CONSTS = "data_pipeline.scraper.initiatives.consts"


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

    # Resolve the two paths we need before imports so the patches are ready.
    tmp_log_dir = str(tmp_root / "logs")
    tmp_data_dir = str(tmp_root)

    # ── Path mocks ─────────────────────────────────────────────────────────────
    # Patch LOG_DIR  → prevents _logger.py from mkdir-ing inside the real project
    #                  tree when it is first imported below.
    # Patch PIPELINE_DIR → redirects build_timestamped_run_dirs (used internally
    #                  by any module that builds its own run dirs) to tmp as well.
    with (
        patch(f"{_INITIATIVES_CONSTS}.LOG_DIR", tmp_log_dir),
        patch(f"{_INITIATIVES_CONSTS}.PIPELINE_DIR", tmp_data_dir),
    ):
        # ── Deferred imports ──────────────────────────────────────────────────
        # Kept inside the patch block: the first import of browser.py pulls in
        # _logger.py, which reads the (now-patched) LOG_DIR value.
        from data_pipeline.scraper.initiatives.browser import initialize_browser
        from data_pipeline.scraper.initiatives.fetchers.listings import (
            scrape_all_listings,
        )
        from data_pipeline.scraper.initiatives.fetchers.ecis import (
            download_all_initiatives,
        )
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

        # ── Build run directories under tmp ───────────────────────────────────
        dirs = build_timestamped_run_dirs(
            tmp_data_dir,
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

        # ── Scraping mocks ────────────────────────────────────────────────────
        _original_parse = data_parser.parse_initiatives_list_data

        def _limited_parse(page_source: str, base_url: str) -> list:
            return _original_parse(page_source, base_url)[:MAX_INITIATIVES_E2E]

        def _stop_at_first_page(driver, current_page: int) -> bool:
            return False

        # ── Live scrape ───────────────────────────────────────────────────────
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

            updated_data, _ = download_all_initiatives(
                driver, pages_dir, initiative_data
            )
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
    # pytest owns tmp_root — no manual cleanup needed
