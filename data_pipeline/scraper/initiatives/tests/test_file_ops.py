import os
import pytest
from unittest.mock import MagicMock, patch
from selenium import webdriver

from data_pipeline.scraper.initiatives.file_ops import (
    save_initiative_page,
    save_listing_page,
)
from data_pipeline.scraper.initiatives.consts import LISTING_PAGE_FILENAME_PATTERN
from data_pipeline.consts import DEBUGGING_DIR_NAME

MODULE = "data_pipeline.scraper.initiatives.file_ops"

_URL = "https://host/2023/000001_en"
_EXPECTED_FILENAME = "2023_000001_en.html"
_YEAR = "2023"
_HTML = "<html><body>initiative content</body></html>"

# ── Shared fixtures ────────────────────────────────────────────────────────────


@pytest.fixture
def no_validation():
    """Bypass the MIN_HTML_LENGTH guard that would redirect/raise on short HTML."""
    with patch(f"{MODULE}.validate_html"):
        yield


@pytest.fixture
def debug_name():
    """Inject the missing DEBUGGING_DIR_NAME import into file_ops."""
    with patch(f"{MODULE}.DEBUGGING_DIR_NAME", new=DEBUGGING_DIR_NAME, create=True):
        yield


# ── TestSaveInitiativePage ─────────────────────────────────────────────────────


class TestSaveInitiativePage:

    def test_returns_expected_filename(self, tmp_path, no_validation):
        filename = save_initiative_page(str(tmp_path), _URL, _HTML)
        assert filename == _EXPECTED_FILENAME

    def test_file_created_in_pages_dir(self, tmp_path, no_validation):
        save_initiative_page(str(tmp_path), _URL, _HTML)
        assert (tmp_path / _YEAR / _EXPECTED_FILENAME).exists()  # ← year subdir

    def test_file_content_contains_source(self, tmp_path, no_validation):
        save_initiative_page(str(tmp_path), _URL, _HTML)
        written = (tmp_path / _YEAR / _EXPECTED_FILENAME).read_text(
            encoding="utf-8"
        )  # ← year subdir
        assert "initiative content" in written

    def test_different_urls_produce_different_filenames(self, tmp_path, no_validation):
        url_a = "https://host/2023/000001_en"
        url_b = "https://host/2022/000002_en"
        name_a = save_initiative_page(str(tmp_path), url_a, _HTML)
        name_b = save_initiative_page(str(tmp_path), url_b, _HTML)
        assert name_a != name_b

    def test_debug_false_saves_to_pages_dir(self, tmp_path, no_validation):
        pages_dir = tmp_path / "pages"
        pages_dir.mkdir()
        save_initiative_page(str(pages_dir), _URL, _HTML, debug=False)
        assert (pages_dir / _YEAR / _EXPECTED_FILENAME).exists()  # ← year subdir

    def test_debug_true_does_not_save_to_pages_dir(
        self, tmp_path, no_validation, debug_name
    ):
        pages_dir = tmp_path / "pages"
        pages_dir.mkdir()
        save_initiative_page(str(pages_dir), _URL, _HTML, debug=True)
        assert not (pages_dir / _YEAR / _EXPECTED_FILENAME).exists()

    def test_debug_true_creates_file_in_debug_dir(
        self, tmp_path, no_validation, debug_name
    ):
        pages_dir = tmp_path / "pages"
        pages_dir.mkdir()
        save_initiative_page(str(pages_dir), _URL, _HTML, debug=True)
        expected_debug_dir = tmp_path / DEBUGGING_DIR_NAME / "pages"
        assert any(expected_debug_dir.rglob("*.html"))


# ── TestSaveListingPage ────────────────────────────────────────────────────────


class TestSaveListingPage:

    def test_returns_two_element_tuple(self, mock_driver, tmp_path, no_validation):
        result = save_listing_page(mock_driver, str(tmp_path), 1)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_first_element_is_the_page_source(
        self, mock_driver, tmp_path, no_validation
    ):
        mock_driver.page_source = _HTML
        source, _ = save_listing_page(mock_driver, str(tmp_path), 1)
        assert source == _HTML

    def test_second_element_is_existing_file_path(
        self, mock_driver, tmp_path, no_validation
    ):
        _, path = save_listing_page(mock_driver, str(tmp_path), 1)
        assert os.path.isfile(path)

    def test_saved_file_is_inside_list_dir(self, mock_driver, tmp_path, no_validation):
        _, path = save_listing_page(mock_driver, str(tmp_path), 1)
        assert os.path.commonpath([path, str(tmp_path)]) == str(tmp_path)

    def test_filename_matches_pattern_for_given_page(
        self, mock_driver, tmp_path, no_validation
    ):
        page = 5
        expected_filename = LISTING_PAGE_FILENAME_PATTERN.format(page)
        _, path = save_listing_page(mock_driver, str(tmp_path), page)
        assert os.path.basename(path) == expected_filename

    def test_different_page_numbers_produce_different_files(
        self, mock_driver, tmp_path, no_validation
    ):
        _, path1 = save_listing_page(mock_driver, str(tmp_path), 1)
        _, path2 = save_listing_page(mock_driver, str(tmp_path), 2)
        assert path1 != path2

    def test_written_file_contains_page_source(
        self, mock_driver, tmp_path, no_validation
    ):
        mock_driver.page_source = _HTML
        _, path = save_listing_page(mock_driver, str(tmp_path), 1)
        written = open(path, encoding="utf-8").read()
        assert "initiative content" in written
