"""
Session-scoped fixtures for the Commission responses end-to-end test suite.

Strategy: copy the real initiatives pages dir into a temp run dir, then
patch find_newest_scraped_data_dir to return that temp run dir.
The scraper reads HTML from there AND writes all output (responses/, logs/,
CSV) into the same temp dir — no real data directory is touched.
"""

import shutil
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import pytest

from data_pipeline.scraper.responses import html_parser as responses_html_parser
from data_pipeline.scraper.responses import consts as responses_consts

MAX_RESPONSES_E2E = 2

MAIN_MODULE = "data_pipeline.scraper.responses.__main__"
LOCATE_FN = f"{MAIN_MODULE}.find_newest_scraped_data_dir"


@dataclass
class ResponseScrapeArtifacts:
    timestamp: str
    run_dir: Path
    responses_path: Path
    logs_path: Path
    csv_path: Path


@pytest.fixture(scope="session")
def e2e_scrape(tmp_path_factory) -> ResponseScrapeArtifacts:
    from data_pipeline.scraper.responses.__main__ import scrape_commission_responses
    from data_pipeline.pipeline_shared.consts import DATA_DIR, INITIATIVES_DIR_NAME
    from data_pipeline.pipeline_shared.locate_run_dir import (
        find_newest_scraped_data_dir,
    )

    # Resolve the real initiatives run dir BEFORE any patching
    real_run_dir = Path(find_newest_scraped_data_dir(DATA_DIR, INITIATIVES_DIR_NAME))

    # Build a temp run dir and copy the real initiatives pages into it
    tmp_run_dir = tmp_path_factory.mktemp("eci_responses_e2e")
    shutil.copytree(
        real_run_dir / INITIATIVES_DIR_NAME,
        tmp_run_dir / INITIATIVES_DIR_NAME,
    )

    original_extract = (
        responses_html_parser.ResponseLinkExtractor.extract_links_from_directory
    )

    def limited_extract(self, initiatives_dir: str) -> list:
        return original_extract(self, initiatives_dir)[:MAX_RESPONSES_E2E]

    with (
        patch(LOCATE_FN, return_value=str(tmp_run_dir)),
        patch.object(
            responses_html_parser.ResponseLinkExtractor,
            "extract_links_from_directory",
            limited_extract,
        ),
    ):
        timestamp = scrape_commission_responses()

    responses_path = tmp_run_dir / responses_consts.RESPONSES_DIR_NAME

    yield ResponseScrapeArtifacts(
        timestamp=timestamp,
        run_dir=tmp_run_dir,
        responses_path=responses_path,
        logs_path=tmp_run_dir / responses_consts.LOG_DIR_NAME,
        csv_path=responses_path / responses_consts.CSV_FILENAME,
    )
