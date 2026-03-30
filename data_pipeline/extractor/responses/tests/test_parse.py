"""Tests for responses.extractor.parse."""

from unittest.mock import patch

import pytest

from data_pipeline.extractor.extractor_shared.errors import HTMLParseError
from data_pipeline.extractor.responses.extractor.parse import (
    parse_html_files,
)

PARSED_DICT = {
    "commission_answer_text": None,
    "followup_additional_website": None,
    "followup_events": None,
    "legislation_passed": None,
}


class TestParseHtmlFiles:

    def test_returns_dict_keyed_by_reg_number(self, tmp_path):

        html_files = {"2020/000001": tmp_path / "2020_000001_en.html"}

        with patch(
            "data_pipeline.extractor.responses.extractor.parse.parse_HTML",
            return_value=PARSED_DICT,
        ):

            result = parse_html_files(html_files)

        assert result["2020/000001"] == PARSED_DICT

    def test_processes_multiple_files(self, tmp_path):

        html_files = {
            "2020/000001": tmp_path / "2020_000001_en.html",
            "2021/000002": tmp_path / "2021_000002_en.html",
        }
        with patch(
            "data_pipeline.extractor.responses.extractor.parse.parse_HTML",
            return_value=PARSED_DICT,
        ):

            result = parse_html_files(html_files)

        assert len(result) == 2

    def test_raises_html_parse_error_on_failure(self, tmp_path):

        html_files = {"2020/000001": tmp_path / "2020_000001_en.html"}

        with patch(
            "data_pipeline.extractor.responses.extractor.parse.parse_HTML",
            side_effect=ValueError("bad HTML"),
        ):

            with pytest.raises(
                HTMLParseError, match="Failed to parse HTML for 2020/000001"
            ):
                parse_html_files(html_files)

    def test_html_parse_error_chains_original_exception(self, tmp_path):

        original = RuntimeError("underlying error")
        html_files = {"2020/000001": tmp_path / "2020_000001_en.html"}

        with patch(
            "data_pipeline.extractor.responses.extractor.parse.parse_HTML",
            side_effect=original,
        ):

            with pytest.raises(HTMLParseError) as exc_info:
                parse_html_files(html_files)

        assert exc_info.value.__cause__ is original

    def test_empty_html_files_returns_empty_dict(self):

        with patch("data_pipeline.extractor.responses.extractor.parse.parse_HTML"):
            result = parse_html_files({})

        assert not result
