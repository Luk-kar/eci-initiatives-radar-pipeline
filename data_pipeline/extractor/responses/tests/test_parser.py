"""Tests for responses.extractor.parser (parse_HTML)."""

from contextlib import contextmanager, ExitStack
from unittest.mock import patch

import pytest

from data_pipeline.extractor.responses.extractor.parser.model import (
    ECIResponseParseHTMLRecord,
)
from data_pipeline.extractor.responses.extractor.parser import parse_HTML

HTML = "<html><body><p>Commission response.</p></body></html>"


def _write_html(tmp_path, content=HTML):

    f = tmp_path / "2020_000001_en.html"
    f.write_text(content, encoding="utf-8")
    return f


@contextmanager
def _mock_extractors(ca=None, fw=None, fe=None, lp=None):
    with ExitStack() as stack:
        stack.enter_context(
            patch(
                "data_pipeline.extractor.responses.extractor.parser.extract_commission_answer",
                return_value=ca,
            )
        )
        stack.enter_context(
            patch(
                "data_pipeline.extractor.responses.extractor.parser.extract_followup_additional_website",
                return_value=fw,
            )
        )
        stack.enter_context(
            patch(
                "data_pipeline.extractor.responses.extractor.parser.extract_followup_events",
                return_value=fe,
            )
        )
        stack.enter_context(
            patch(
                "data_pipeline.extractor.responses.extractor.parser.extract_legislation_passed",
                return_value=lp,
            )
        )
        stack.enter_context(
            patch(
                "data_pipeline.extractor.responses.extractor.parser.FILE_ENCODING",
                "utf-8",
            )
        )
        yield


class TestParseHTML:
    def test_returns_dict_with_model_fields(self, tmp_path):

        html_file = _write_html(tmp_path)

        with _mock_extractors():

            result = parse_HTML(html_file, "2020/000001")

        assert set(result.keys()) == set(ECIResponseParseHTMLRecord.model_fields.keys())

    def test_commission_answer_text_in_result(self, tmp_path):

        html_file = _write_html(tmp_path)

        with _mock_extractors(ca=["The Commission responds."]):

            result = parse_HTML(html_file, "2020/000001")

        commission_answer_text = result["commission_answer_text"]

        assert isinstance(commission_answer_text, list)
        assert all(isinstance(item, str) for item in commission_answer_text)
        assert len(commission_answer_text) == 1

        assert commission_answer_text == ["The Commission responds."]

    def test_list_fields_preserved(self, tmp_path):

        html_file = _write_html(tmp_path)

        with _mock_extractors(
            fw="https://followup.example.com",
            fe=["Event 1", "Event 2"],
            lp=["Regulation (EU) 1/2020"],
        ):

            result = parse_HTML(html_file, "2020/000001")

        assert result["followup_additional_website"] == "https://followup.example.com"
        assert result["followup_events"] == ["Event 1", "Event 2"]
        assert result["legislation_passed"] == ["Regulation (EU) 1/2020"]

    def test_missing_file_raises(self, tmp_path):

        with pytest.raises(FileNotFoundError):
            parse_HTML(tmp_path / "missing.html", "2020/000001")
