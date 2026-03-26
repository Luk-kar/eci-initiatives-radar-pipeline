"""
Light-weight end-to-end tests against the live EU Commission server.

Validates the complete responses scraping pipeline produces the expected
file artifacts. The session fixture keeps total server load to
MAX_RESPONSES_E2E Commission response pages.

What is tested:
    - Directory structure (responses/, logs/)
    - CSV created with required columns, slash-format registration numbers,
      and non-empty datetimes on successful downloads
    - Individual response HTML files organised in 4-digit year directories
    - HTML content is non-trivial and references the Commission domain

What is NOT tested:
    - Detailed link extraction edge-cases (covered by unit tests)
    - Rate-limit recovery paths (covered by unit tests)
    - Exact row counts or specific content values (change on the live site)

Expected runtime: 15 – 60 seconds.
"""

import csv
from pathlib import Path

import pytest

from data_pipeline.pipeline_shared.consts import FILE_ENCODING
from data_pipeline.scraper.responses.consts import CSV_FIELDNAMES

pytestmark = pytest.mark.e2e


# ── Helpers ────────────────────────────────────────────────────────────────────


def _collect_response_html_files(responses_path: Path) -> list[Path]:
    """Return all .html files nested one level under responses_path (year dirs)."""

    result = []

    if not responses_path.exists():
        return result

    for year_dir in responses_path.iterdir():
        if year_dir.is_dir():
            result.extend(year_dir.glob("*.html"))

    return result


def _read_csv_rows(csv_path: Path) -> list[dict]:

    with open(csv_path, encoding=FILE_ENCODING) as f:
        return list(csv.DictReader(f))


# ── Tests ──────────────────────────────────────────────────────────────────────


class TestDirectoryStructure:
    """Verify that all expected output directories are created."""

    def test_data_root_exists(self, e2e_scrape):

        assert e2e_scrape.run_dir.exists(), f"Run dir not found: {e2e_scrape.run_dir}"

    def test_responses_dir_exists(self, e2e_scrape):

        assert (
            e2e_scrape.responses_path.exists()
        ), f"Responses dir not found: {e2e_scrape.responses_path}"

    def test_logs_dir_exists(self, e2e_scrape):

        assert (
            e2e_scrape.logs_path.exists()
        ), f"Logs dir not found: {e2e_scrape.logs_path}"


class TestCsvArtifacts:
    """Validate the responses CSV structure and content."""

    def test_csv_file_created(self, e2e_scrape):

        assert e2e_scrape.csv_path.exists(), f"CSV not found: {e2e_scrape.csv_path}"

    def test_csv_has_all_required_columns(self, e2e_scrape):

        with open(e2e_scrape.csv_path, encoding=FILE_ENCODING) as f:
            actual = csv.DictReader(f).fieldnames or []

        for col in CSV_FIELDNAMES:
            assert col in actual, f"Required column {col!r} missing from CSV"

    def test_csv_contains_rows(self, e2e_scrape):

        rows = _read_csv_rows(e2e_scrape.csv_path)
        assert len(rows) > 0, "CSV has no data rows"

    def test_csv_registration_numbers_use_slash_format(self, e2e_scrape):
        """write_responses_csv normalises underscores → slashes (e.g. 2019/000007)."""

        rows = _read_csv_rows(e2e_scrape.csv_path)

        for row in rows:
            reg = row["registration_number"]
            if reg:
                assert "/" in reg, f"Registration number not in slash format: {reg!r}"

    def test_successful_rows_have_datetime_set(self, e2e_scrape):

        rows = _read_csv_rows(e2e_scrape.csv_path)
        downloaded = [r for r in rows if r.get("datetime")]
        assert len(downloaded) > 0, "No rows with a populated datetime found"

    def test_csv_urls_are_non_empty(self, e2e_scrape):

        rows = _read_csv_rows(e2e_scrape.csv_path)

        for row in rows:
            assert row[
                "url_find_initiative"
            ].strip(), "Found a row with an empty url_find_initiative"


class TestResponsePageArtifacts:
    """Validate the individually downloaded Commission response HTML files."""

    def test_response_html_files_downloaded(self, e2e_scrape):

        html_files = _collect_response_html_files(e2e_scrape.responses_path)

        assert (
            len(html_files) > 0
        ), f"No response HTML files found under {e2e_scrape.responses_path}"

    def test_year_directories_are_4_digit(self, e2e_scrape):

        for item in e2e_scrape.responses_path.iterdir():

            if item.is_dir():
                assert (
                    item.name.isdigit() and len(item.name) == 4
                ), f"Year directory {item.name!r} is not 4 digits"

    def test_response_filenames_end_with_en(self, e2e_scrape):

        for html_path in _collect_response_html_files(e2e_scrape.responses_path):

            assert html_path.stem.endswith(
                "_en"
            ), f"Response filename doesn't end with _en: {html_path.name!r}"

    def test_response_html_is_non_trivial(self, e2e_scrape):

        for html_path in _collect_response_html_files(e2e_scrape.responses_path):

            content = html_path.read_text(encoding=FILE_ENCODING)
            assert (
                len(content) > 1_000
            ), f"HTML file suspiciously small ({len(content)} chars): {html_path.name}"

    def test_response_html_has_html_tags(self, e2e_scrape):

        for html_path in _collect_response_html_files(e2e_scrape.responses_path):

            content = html_path.read_text(encoding=FILE_ENCODING).lower()
            assert "<html" in content, f"No <html> tag in {html_path.name}"
            assert "</html>" in content, f"No </html> tag in {html_path.name}"

    def test_response_html_references_commission_domain(self, e2e_scrape):

        commission_markers = (
            "commission.europa.eu",
            "European Commission",
        )

        for html_path in _collect_response_html_files(e2e_scrape.responses_path):
            content = html_path.read_text(encoding=FILE_ENCODING)
            assert any(
                m in content for m in commission_markers
            ), f"No Commission domain marker found in {html_path.name}"
