"""
Tests for Commission response page HTML save operations.

Validates the normal save path, debug directory routing, filename
format, and the validate → prettify → write pipeline.
"""

import os
from unittest.mock import patch

import pytest

from data_pipeline.scraper.responses.file_operations.page import save_response_page
from data_pipeline.pipeline_shared.consts import FILE_ENCODING

MODULE = "data_pipeline.scraper.responses.file_operations.page"

YEAR = "2023"
REG_NUMBER = "000007"
HTML = "<html><body><p>Commission response content</p></body></html>"


# Patching validate_html lets us test filesystem behaviour in isolation;
# HTML validation has its own tests in scraper_shared.
@pytest.fixture
def no_validation():

    with patch(f"{MODULE}.validate_html"):
        yield


# ── TestSaveResponsePage ───────────────────────────────────────────────────────


@pytest.mark.usefixtures("no_validation")
class TestSaveResponsePage:
    """
    Validates that save_response_page writes files to the correct location
    and returns the expected relative filename.
    """

    def test_returns_relative_filename(self, tmp_path):
        result = save_response_page(str(tmp_path), YEAR, REG_NUMBER, HTML)

        assert result == f"{YEAR}/{REG_NUMBER}_en.html"

    def test_file_is_written_to_year_subdirectory(self, tmp_path):

        save_response_page(str(tmp_path), YEAR, REG_NUMBER, HTML)
        expected = tmp_path / YEAR / f"{REG_NUMBER}_en.html"

        assert expected.exists()

    def test_written_file_contains_page_source(self, tmp_path):

        save_response_page(str(tmp_path), YEAR, REG_NUMBER, HTML)
        path = tmp_path / YEAR / f"{REG_NUMBER}_en.html"

        content = path.read_text(encoding=FILE_ENCODING)
        assert "Commission response content" in content

    def test_year_directory_is_created(self, tmp_path):

        save_response_page(str(tmp_path), YEAR, REG_NUMBER, HTML)

        assert (tmp_path / YEAR).is_dir()

    def test_different_reg_numbers_produce_different_files(self, tmp_path):

        save_response_page(str(tmp_path), YEAR, "000001", HTML)
        save_response_page(str(tmp_path), YEAR, "000002", HTML)

        assert (tmp_path / YEAR / "000001_en.html").exists()
        assert (tmp_path / YEAR / "000002_en.html").exists()


@pytest.mark.usefixtures("no_validation")
class TestSaveResponsePageDebug:
    """
    Validates that debug=True redirects output to the debugging subtree
    without touching the normal output directory.
    """

    def test_debug_file_written_to_debugging_subtree(self, tmp_path):

        responses_dir = tmp_path / "responses"
        responses_dir.mkdir()

        save_response_page(str(responses_dir), YEAR, REG_NUMBER, HTML, debug=True)

        debug_path = (
            tmp_path / "debugging" / "responses" / YEAR / f"{REG_NUMBER}_en.html"
        )
        assert debug_path.exists()

    def test_debug_does_not_write_to_normal_dir(self, tmp_path):

        responses_dir = tmp_path / "responses"
        responses_dir.mkdir()

        save_response_page(str(responses_dir), YEAR, REG_NUMBER, HTML, debug=True)

        normal_path = responses_dir / YEAR / f"{REG_NUMBER}_en.html"
        assert not normal_path.exists()

    def test_debug_returns_same_relative_filename(self, tmp_path):

        responses_dir = tmp_path / "responses"
        responses_dir.mkdir()

        result = save_response_page(
            str(responses_dir), YEAR, REG_NUMBER, HTML, debug=True
        )

        assert result == f"{YEAR}/{REG_NUMBER}_en.html"
