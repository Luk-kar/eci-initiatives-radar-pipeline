# data_pipeline/scraper/initiatives/tests/end_to_end/conftest.py
"""Session-scoped fixtures for the initiatives end-to-end test suite.

Runs a deliberately limited live scrape against the EU server:
  - exactly 1 listing page  (pagination mocked to stop early)
  - MAX_INITIATIVES_E2E individual initiative pages

LOGDIR and PIPELINE_DIR are already redirected to a temp directory by the
autouse fixture in data_pipeline.scraper.initiatives.conftest.py. This fixture
handles only the e2e-specific scraping mocks and delegates the full pipeline
execution to scrape_eci_initiatives().
"""
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import pytest

# Tuning
MAX_INITIATIVES_E2E = 2

# Patch targets
LISTINGS_FETCHER = "data_pipeline.scraper.initiatives.fetchers.listings.fetcher"
MAIN_MODULE = "data_pipeline.scraper.initiatives.__main__"


@dataclass
class ScrapeArtifacts:
    timestamp: str
    data_path: Path
    listings_path: Path
    pages_path: Path
    logs_path: Path


@pytest.fixture(scope="session")
def e2e_scrape(tmp_path_factory) -> ScrapeArtifacts:
    """Run a limited live scrape via scrape_eci_initiatives; output lands in a temp directory."""
    import data_pipeline.scraper.initiatives.consts as initiatives_consts
    from data_pipeline.scraper.initiatives.__main__ import scrape_eci_initiatives
    from data_pipeline.scraper.initiatives import data_parser

    tmp_root = tmp_path_factory.mktemp("eci_e2e")
    original_parse = data_parser.parse_initiatives_list_data

    def limited_parse(pagesource: str, baseurl: str) -> list:
        return original_parse(pagesource, baseurl)[:MAX_INITIATIVES_E2E]

    def stop_at_first_page(driver, currentpage: int) -> bool:
        return False

    with (
        patch(f"{MAIN_MODULE}.PIPELINE_DIR", str(tmp_root)),
        patch(
            f"{LISTINGS_FETCHER}.parse_initiatives_list_data", side_effect=limited_parse
        ),
        patch(
            f"{LISTINGS_FETCHER}.navigate_to_next_page", side_effect=stop_at_first_page
        ),
    ):
        timestamp = scrape_eci_initiatives()

    run_dir = tmp_root / initiatives_consts.DATA_DIR_NAME / timestamp
    yield ScrapeArtifacts(
        timestamp=timestamp,
        data_path=run_dir,
        listings_path=run_dir / initiatives_consts.LISTINGS_DIR_NAME,
        pages_path=run_dir / initiatives_consts.PAGES_DIR_NAME,
        logs_path=Path(initiatives_consts.LOG_DIR),
    )
