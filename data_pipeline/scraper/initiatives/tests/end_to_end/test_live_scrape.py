"""
Light-weight end-to-end tests against the live EU server.

Validates the complete initiatives scraping pipeline produces the expected
file artifacts without testing fine-grained parsing details.
The session fixture keeps total server load to 1 listing page + 2 initiative pages.

What is tested:
    - Directory structure (data/, listings/, initiatives/, logs/)
    - Listing HTML file created with the correct filename prefix
    - CSV created with the required columns, valid URL format, and non-empty
      registration numbers
    - Individual initiative HTML files organised in 4-digit year directories
    - HTML content is non-trivial and references the ECI domain

What is NOT tested:
    - Detailed parsing edge-cases (covered by unit tests)
    - Rate-limit recovery paths (covered by unit tests)
    - Exact row counts or specific content values (these change on the live site)

Expected runtime: 30 – 90 seconds.
"""

# Standard library
import csv
import os
from pathlib import Path

# Third-party
import pytest

# Local
from data_pipeline.scraper.initiatives.consts import CSV_FIELDNAMES, CSV_FILENAME
from data_pipeline.scraper.scraper_shared.consts import BASE_URL

from data_pipeline.pipeline_shared.consts import FILE_ENCODING

pytestmark = pytest.mark.e2e


# ── Helpers ────────────────────────────────────────────────────────────────────


def _collect_initiative_html_files(pages_path: Path) -> list[Path]:
    """Return all .html files nested one level under pages_path (year dirs)."""

    result = []

    if not pages_path.exists():
        return result

    for year_dir in pages_path.iterdir():

        if year_dir.is_dir():
            result.extend(year_dir.glob("*.html"))

    return result


def _read_csv_rows(csv_path: Path) -> list[dict]:
    with open(csv_path, encoding=FILE_ENCODING) as f:
        return list(csv.DictReader(f))


# ── Tests ──────────────────────────────────────────────────────────────────────


class TestDirectoryStructure:
    """Verify that all expected top-level directories are created."""

    def test_data_root_exists(self, e2e_scrape):

        assert (
            e2e_scrape.data_path.exists()
        ), f"Data root not found: {e2e_scrape.data_path}"

    def test_listings_dir_exists(self, e2e_scrape):

        assert (
            e2e_scrape.listings_path.exists()
        ), f"Listings dir not found: {e2e_scrape.listings_path}"

    def test_pages_dir_exists(self, e2e_scrape):

        assert (
            e2e_scrape.pages_path.exists()
        ), f"Pages dir not found: {e2e_scrape.pages_path}"

    def test_logs_dir_exists(self, e2e_scrape):

        assert (
            e2e_scrape.logs_path.exists()
        ), f"Logs dir not found: {e2e_scrape.logs_path}"


class TestListingArtifacts:
    """Validate the listing HTML file and the generated CSV."""

    # ── Listing HTML ──────────────────────────────────────────────────────────

    def test_listing_html_file_created(self, e2e_scrape):

        html_files = list(e2e_scrape.listings_path.glob("*.html"))
        assert (
            len(html_files) >= 1
        ), f"No listing HTML files found in {e2e_scrape.listings_path}"

    def test_listing_html_filename_prefix(self, e2e_scrape):

        expected_prefix = "Find_initiative_European_Citizens_Initiative_page_"
        for f in e2e_scrape.listings_path.glob("*.html"):
            assert f.name.startswith(
                expected_prefix
            ), f"Unexpected listing filename: {f.name!r}"

    # ── CSV existence ─────────────────────────────────────────────────────────

    def test_csv_file_created(self, e2e_scrape):

        csv_path = e2e_scrape.listings_path / CSV_FILENAME
        assert csv_path.exists(), f"{CSV_FILENAME!r} not found in listings dir"

    # ── CSV structure ─────────────────────────────────────────────────────────

    def test_csv_has_all_required_columns(self, e2e_scrape):

        csv_path = e2e_scrape.listings_path / CSV_FILENAME
        with open(csv_path, encoding=FILE_ENCODING) as f:
            reader = csv.DictReader(f)
            actual = reader.fieldnames or []
        for col in CSV_FIELDNAMES:
            assert col in actual, f"Required column {col!r} missing from CSV"

    def test_csv_contains_rows(self, e2e_scrape):

        rows = _read_csv_rows(e2e_scrape.listings_path / CSV_FILENAME)
        assert len(rows) > 0, "CSV has no data rows"

    # ── CSV content ───────────────────────────────────────────────────────────

    def test_csv_urls_point_to_eci_initiative_details(self, e2e_scrape):

        rows = _read_csv_rows(e2e_scrape.listings_path / CSV_FILENAME)
        expected_prefix = f"{BASE_URL}/initiatives/details/"

        for row in rows:

            assert row["url"].startswith(
                expected_prefix
            ), f"Unexpected URL: {row['url']!r}"

    def test_csv_registration_numbers_nonempty(self, e2e_scrape):

        rows = _read_csv_rows(e2e_scrape.listings_path / CSV_FILENAME)

        for row in rows:

            assert row[
                "registration_number"
            ].strip(), f"Empty registration_number for {row['url']}"

    def test_csv_current_status_nonempty(self, e2e_scrape):

        rows = _read_csv_rows(e2e_scrape.listings_path / CSV_FILENAME)

        for row in rows:

            assert row[
                "current_status"
            ].strip(), f"Empty current_status for {row['url']}"


class TestInitiativePageArtifacts:
    """Validate the individually downloaded initiative HTML files."""

    def test_initiative_html_files_downloaded(self, e2e_scrape):

        html_files = _collect_initiative_html_files(e2e_scrape.pages_path)

        assert (
            len(html_files) > 0
        ), f"No initiative HTML files found under {e2e_scrape.pages_path}"

    def test_year_directories_are_4_digit(self, e2e_scrape):

        for item in e2e_scrape.pages_path.iterdir():

            if item.is_dir():
                assert (
                    item.name.isdigit() and len(item.name) == 4
                ), f"Year directory {item.name!r} is not 4 digits"

    def test_initiative_filenames_contain_underscore(self, e2e_scrape):

        for html_path in _collect_initiative_html_files(e2e_scrape.pages_path):

            assert (
                "_" in html_path.stem
            ), f"Initiative filename missing underscore: {html_path.name!r}"

    def test_initiative_html_is_non_trivial(self, e2e_scrape):

        for html_path in _collect_initiative_html_files(e2e_scrape.pages_path):

            content = html_path.read_text(encoding=FILE_ENCODING)
            assert (
                len(content) > 1_000
            ), f"HTML file suspiciously small ({len(content)} chars): {html_path.name}"

    def test_initiative_html_has_html_tags(self, e2e_scrape):

        for html_path in _collect_initiative_html_files(e2e_scrape.pages_path):

            content = html_path.read_text(encoding=FILE_ENCODING).lower()
            assert "<html" in content, f"No <html> tag in {html_path.name}"
            assert "</html>" in content, f"No </html> tag in {html_path.name}"

    def test_initiative_html_references_eci_domain(self, e2e_scrape):

        eci_markers = (
            "citizens-initiative.europa.eu",
            "European Citizens\u2019 Initiative",
            "European Citizens' Initiative",
        )

        for html_path in _collect_initiative_html_files(e2e_scrape.pages_path):

            content = html_path.read_text(encoding=FILE_ENCODING)
            assert any(
                m in content for m in eci_markers
            ), f"No ECI domain marker found in {html_path.name}"
