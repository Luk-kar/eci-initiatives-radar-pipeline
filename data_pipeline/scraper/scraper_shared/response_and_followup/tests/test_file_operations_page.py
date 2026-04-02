"""Behavioural tests for save_response_page (single authoritative suite)."""

import logging
from unittest.mock import patch

import pytest

from data_pipeline.scraper.scraper_shared.response_and_followup.file_operations.page import (
    save_response_page,
)
from data_pipeline.pipeline_shared.consts import FILE_ENCODING

MODULE = (
    "data_pipeline.scraper.scraper_shared.response_and_followup.file_operations.page"
)
YEAR, REG_NUMBER = "2023", "000007"
HTML = "<html><body><p>Commission response content</p></body></html>"
_logger = logging.getLogger(__name__)


@pytest.fixture
def no_validation():

    with patch(f"{MODULE}.validate_html"):
        yield


@pytest.mark.usefixtures("no_validation")
class TestSaveResponsePage:

    def test_returns_relative_filename(self, tmp_path):

        result = save_response_page(
            str(tmp_path), YEAR, REG_NUMBER, HTML, logger=_logger
        )
        assert result == f"{YEAR}_{REG_NUMBER}.html"

    def test_file_written_to_year_subdirectory(self, tmp_path):

        save_response_page(str(tmp_path), YEAR, REG_NUMBER, HTML, logger=_logger)
        assert (tmp_path / YEAR / f"{YEAR}_{REG_NUMBER}.html").exists()

    def test_written_file_contains_page_source(self, tmp_path):

        save_response_page(str(tmp_path), YEAR, REG_NUMBER, HTML, logger=_logger)
        content = (tmp_path / YEAR / f"{YEAR}_{REG_NUMBER}.html").read_text(
            encoding=FILE_ENCODING
        )
        assert "Commission response content" in content

    def test_year_directory_is_created(self, tmp_path):

        save_response_page(str(tmp_path), YEAR, REG_NUMBER, HTML, logger=_logger)

        assert (tmp_path / YEAR).is_dir()

    def test_different_reg_numbers_produce_different_files(self, tmp_path):

        save_response_page(str(tmp_path), YEAR, "000001", HTML, logger=_logger)
        save_response_page(str(tmp_path), YEAR, "000002", HTML, logger=_logger)

        assert (tmp_path / YEAR / f"{YEAR}_000001.html").exists()
        assert (tmp_path / YEAR / f"{YEAR}_000002.html").exists()


@pytest.mark.usefixtures("no_validation")
class TestSaveResponsePageDebug:

    def test_debug_file_written_to_debugging_subtree(self, tmp_path):

        responses_dir = tmp_path / "responses"
        responses_dir.mkdir()
        save_response_page(
            str(responses_dir), YEAR, REG_NUMBER, HTML, debug=True, logger=_logger
        )

        assert (
            tmp_path / "debugging" / "responses" / YEAR / f"{YEAR}_{REG_NUMBER}.html"
        ).exists()

    def test_debug_does_not_write_to_normal_dir(self, tmp_path):

        responses_dir = tmp_path / "responses"
        responses_dir.mkdir()
        save_response_page(
            str(responses_dir), YEAR, REG_NUMBER, HTML, debug=True, logger=_logger
        )

        assert not (responses_dir / YEAR / f"{REG_NUMBER}.html").exists()

    def test_debug_returns_same_relative_filename(self, tmp_path):

        responses_dir = tmp_path / "responses"
        responses_dir.mkdir()
        result = save_response_page(
            str(responses_dir), YEAR, REG_NUMBER, HTML, debug=True, logger=_logger
        )

        assert result == f"{YEAR}_{REG_NUMBER}.html"
