"""Tests for responses_followup.extractor.parser (parse_HTML)."""

from contextlib import contextmanager, ExitStack
from unittest.mock import patch

import pytest


from data_pipeline.extractor.responses_followup.extractor.parser.model import (
    ECIFollowupParseHTMLRecord,
)


from data_pipeline.extractor.responses_followup.extractor.parser import parse_HTML

HTML = "<html><body><p>Commission response.</p></body></html>"


def _write_html(tmp_path, content=HTML):

    f = tmp_path / "2020_000001_en.html"
    f.write_text(content, encoding="utf-8")
    return f


@contextmanager
def _mock_extractors(ca=None, fe=None):
    """
    Mock the two active extractor functions in the parser module.

    FIX: removed mocks for 'extract_followup_additional_website' and
         'extract_linked_policies' — neither function exists in the current
         parser.fields module.  Only 'extract_commission_answer' and
         'extract_followup_events' are imported and called.
    """
    with ExitStack() as stack:
        stack.enter_context(
            patch(
                "data_pipeline.extractor.responses_followup.extractor.parser.extract_commission_answer",
                return_value=ca,
            )
        )
        stack.enter_context(
            patch(
                "data_pipeline.extractor.responses_followup.extractor.parser.extract_followup_events",
                return_value=fe,
            )
        )
        stack.enter_context(
            patch(
                "data_pipeline.extractor.responses_followup.extractor.parser.FILE_ENCODING",
                "utf-8",
            )
        )
        yield


class TestParseHTML:

    def test_returns_dict_with_model_fields(self, tmp_path):

        html_file = _write_html(tmp_path)

        with _mock_extractors():

            result = parse_HTML(html_file, "2020/000001")

        assert set(result.keys()) == set(ECIFollowupParseHTMLRecord.model_fields.keys())

    def test_commission_answer_in_result(self, tmp_path):

        html_file = _write_html(tmp_path)

        with _mock_extractors(ca=["The Commission responds."]):

            result = parse_HTML(html_file, "2020/000001")

        commission_answer = result["commission_answer"]

        assert isinstance(commission_answer, list)
        assert all(isinstance(item, str) for item in commission_answer)
        assert len(commission_answer) == 1
        assert commission_answer == ["The Commission responds."]

    def test_list_fields_preserved(self, tmp_path):

        html_file = _write_html(tmp_path)

        with _mock_extractors(
            ca=["Commission answer text here."],
            fe=["Event 1", "Event 2"],
        ):

            result = parse_HTML(html_file, "2020/000001")

        assert result["commission_answer"] == ["Commission answer text here."]
        assert result["followup_events"] == ["Event 1", "Event 2"]

    def test_missing_file_raises(self, tmp_path):

        with pytest.raises(FileNotFoundError):
            parse_HTML(tmp_path / "missing.html", "2020/000001")
