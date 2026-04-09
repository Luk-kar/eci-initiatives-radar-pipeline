"""
Tests for file operation utilities in the ECI initiatives scraper.

This module verifies the functionality of saving scraped HTML content
to the local filesystem. It ensures that both individual initiative pages
and listing pages are correctly named, properly structured into directories,
and that their contents are accurately written to disk, including the proper
handling of debugging modes.
"""

# Python
import os
from unittest.mock import patch

# Third-party
import pytest

# Local
from data_pipeline.scraper.initiatives.file_operations import (
    save_initiative_page,
    save_listing_page,
)
from data_pipeline.scraper.initiatives.consts import LISTING_PAGE_FILENAME_PATTERN
from data_pipeline.pipeline_shared.consts import DEBUGGING_DIR_NAME

from data_pipeline.pipeline_shared.consts import FILE_ENCODING

MODULE = "data_pipeline.scraper.initiatives.file_operations"

URL = "https://host/2023/000001_en"
EXPECTED_FILENAME = "2023_000001.html"
YEAR = "2023"
HTML = "<html><body>initiative content</body></html>"

# ── Shared fixtures ────────────────────────────────────────────────────────────


@pytest.fixture
def no_validation():
    """Bypass the MIN_HTML_LENGTH guard that would redirect/raise on short HTML."""
    with patch(f"{MODULE}.validate_html"):
        yield


@pytest.fixture
def debug_name():
    """Inject the missing DEBUGGING_DIR_NAME import into file_operations."""
    with patch(f"{MODULE}.DEBUGGING_DIR_NAME", new=DEBUGGING_DIR_NAME, create=True):
        yield


# ── TestSaveInitiativePage ─────────────────────────────────────────────────────


@pytest.mark.usefixtures("no_validation")
class TestSaveInitiativePage:
    """
    Test suite for saving individual ECI initiative detail pages.

    Validates that `save_initiative_page` correctly extracts the year and
    reference ID from the URL to generate proper filenames, creates appropriate
    year-based subdirectories, writes the expected HTML content, and routes files
    to the designated debugging directory when debug mode is enabled.
    """

    def test_returns_expected_filename(self, tmp_path):
        filename = save_initiative_page(str(tmp_path), URL, HTML)
        assert filename == EXPECTED_FILENAME

    def test_file_created_in_pages_dir(self, tmp_path):
        save_initiative_page(str(tmp_path), URL, HTML)
        assert (tmp_path / YEAR / EXPECTED_FILENAME).exists()  # ← year subdir

    def test_file_content_contains_source(self, tmp_path):
        save_initiative_page(str(tmp_path), URL, HTML)
        written = (tmp_path / YEAR / EXPECTED_FILENAME).read_text(
            encoding=FILE_ENCODING
        )  # ← year subdir
        assert "initiative content" in written

    def test_different_urls_produce_different_filenames(self, tmp_path):
        url_a = "https://host/2023/000001_en"
        url_b = "https://host/2022/000002_en"
        name_a = save_initiative_page(str(tmp_path), url_a, HTML)
        name_b = save_initiative_page(str(tmp_path), url_b, HTML)
        assert name_a != name_b

    def test_debug_false_saves_to_pages_dir(self, tmp_path):
        pages_dir = tmp_path / "pages"
        pages_dir.mkdir()
        save_initiative_page(str(pages_dir), URL, HTML, debug=False)
        assert (pages_dir / YEAR / EXPECTED_FILENAME).exists()  # ← year subdir

    @pytest.mark.usefixtures("debug_name")
    def test_debug_true_does_not_save_to_pages_dir(self, tmp_path):
        pages_dir = tmp_path / "pages"
        pages_dir.mkdir()
        save_initiative_page(str(pages_dir), URL, HTML, debug=True)
        assert not (pages_dir / YEAR / EXPECTED_FILENAME).exists()

    @pytest.mark.usefixtures("debug_name")
    def test_debug_true_creates_file_in_debug_dir(self, tmp_path):
        pages_dir = tmp_path / "pages"
        pages_dir.mkdir()
        save_initiative_page(str(pages_dir), URL, HTML, debug=True)
        expected_debug_dir = tmp_path / DEBUGGING_DIR_NAME / "pages"
        assert any(expected_debug_dir.rglob("*.html"))


# ── TestSaveListingPage ────────────────────────────────────────────────────────


@pytest.mark.usefixtures("no_validation")
class TestSaveListingPage:
    """
    Test suite for saving ECI listing and pagination pages.

    Validates that `save_listing_page` correctly extracts the HTML source from
    the WebDriver, generates filenames matching the specified listing page pattern
    (e.g., based on page numbers), writes the content to the target directory,
    and returns both the raw HTML source and the saved file path.
    """

    def test_returns_two_element_tuple(self, mock_driver, tmp_path):

        result = save_listing_page(mock_driver, str(tmp_path), 1)

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_first_element_is_the_page_source(self, mock_driver, tmp_path):

        mock_driver.page_source = HTML
        source, _ = save_listing_page(mock_driver, str(tmp_path), 1)

        assert source == HTML

    def test_second_element_is_existing_file_path(self, mock_driver, tmp_path):

        _, path = save_listing_page(mock_driver, str(tmp_path), 1)

        assert os.path.isfile(path)

    def test_saved_file_is_inside_list_dir(self, mock_driver, tmp_path):

        _, path = save_listing_page(mock_driver, str(tmp_path), 1)

        assert os.path.commonpath([path, str(tmp_path)]) == str(tmp_path)

    def test_filename_matches_pattern_for_given_page(self, mock_driver, tmp_path):

        page = 5
        expected_filename = LISTING_PAGE_FILENAME_PATTERN.format(page)
        _, path = save_listing_page(mock_driver, str(tmp_path), page)

        assert os.path.basename(path) == expected_filename

    def test_different_page_numbers_produce_different_files(
        self, mock_driver, tmp_path
    ):
        _, path1 = save_listing_page(mock_driver, str(tmp_path), 1)
        _, path2 = save_listing_page(mock_driver, str(tmp_path), 2)

        assert path1 != path2

    def test_written_file_contains_page_source(self, mock_driver, tmp_path):

        mock_driver.page_source = HTML
        _, path = save_listing_page(mock_driver, str(tmp_path), 1)

        with open(path, encoding=FILE_ENCODING) as f:
            written = f.read()

        assert "initiative content" in written
