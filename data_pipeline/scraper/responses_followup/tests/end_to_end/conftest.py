"""
Session-scoped fixtures for the Commission responses follow-up end-to-end test suite.

Strategy: find the real eci_responses_*.csv, copy a limited subset of rows
(only those with a non-empty followup_additional_website) into a temp run dir,
then patch _resolve_run_dir_and_csv so the scraper reads from there.
No real data directory is touched during the run.
"""

import csv
import shutil
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import pytest

from data_pipeline.scraper.responses_followup import consts as followup_consts

MAX_RESPONSES_E2E = 2

MAIN_MODULE = "data_pipeline.scraper.responses_followup.__main__"
RESOLVE_FN = f"{MAIN_MODULE}._resolve_run_dir_and_csv"


@dataclass
class ResponseFollowupScrapeArtifacts:
    timestamp: str
    run_dir: Path
    responses_path: Path
    logs_path: Path
    csv_path: Path


def _find_real_csv() -> Path | None:
    """Return the newest eci_responses_*.csv from any run dir, or None."""
    from data_pipeline.pipeline_shared.consts import DATA_DIR

    candidates = sorted(
        DATA_DIR.glob(f"*/{followup_consts.RESPONSES_CSV_GLOB}"),
        reverse=True,
    )
    return candidates[0] if candidates else None


def _write_limited_csv(src_csv: Path, dest_csv: Path, max_rows: int) -> None:
    """Copy up to max_rows rows with non-empty followup_additional_website."""
    from data_pipeline.pipeline_shared.consts import FILE_ENCODING

    with open(src_csv, encoding=FILE_ENCODING, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        valid = [
            row
            for row in reader
            if row.get(followup_consts.FOLLOWUP_URL_COLUMN, "").strip()
        ][:max_rows]

    with open(dest_csv, "w", encoding=FILE_ENCODING, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(valid)


@pytest.fixture(scope="session")
def e2e_scrape(tmp_path_factory) -> ResponseFollowupScrapeArtifacts:
    from data_pipeline.scraper.responses_followup.__main__ import (
        scrape_commission_responses,
    )

    real_csv = _find_real_csv()
    if real_csv is None:
        raise FileNotFoundError(
            f"No '{followup_consts.RESPONSES_CSV_GLOB}' found — "
            "run the extractor first."
        )

    tmp_run_dir = tmp_path_factory.mktemp("eci_responses_followup_e2e")
    tmp_csv = tmp_run_dir / real_csv.name
    _write_limited_csv(real_csv, tmp_csv, MAX_RESPONSES_E2E)

    if tmp_csv.stat().st_size == 0:
        raise RunDirectoryValidationError(
            "No rows with followup_additional_website found in CSV."
        )

    with patch(RESOLVE_FN, return_value=(str(tmp_run_dir), str(tmp_csv))):
        timestamp = scrape_commission_responses()

    responses_path = tmp_run_dir / followup_consts.RESPONSES_DIR_NAME

    yield ResponseFollowupScrapeArtifacts(
        timestamp=timestamp,
        run_dir=tmp_run_dir,
        responses_path=responses_path,
        logs_path=tmp_run_dir / followup_consts.LOG_DIR_NAME,
        csv_path=responses_path / followup_consts.CSV_FILENAME,
    )
