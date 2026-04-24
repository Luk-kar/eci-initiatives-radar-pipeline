from __future__ import annotations

import pytest

from data_pipeline.merger_csv.responses_followup_legislation import assemble
from data_pipeline.merger_csv.responses_followup_legislation.extractor import (
    LegislationResult,
)


class TestParseTextList:
    def test_parse_text_list_returns_items_for_valid_list_literal(self):

        raw = "['alpha', 'beta']"

        actual = assemble.parse_text_list(raw, "commission_answer_text")

        assert actual == ["alpha", "beta"]

    def test_parse_text_list_strips_whitespace_and_skips_empty_items(self):

        raw = "['  alpha  ', '', '   ', None, 'beta']"

        actual = assemble.parse_text_list(raw, "followup_events")

        assert actual == ["alpha", "beta"]

    def test_parsetextlist_returns_empty_list_for_literal_none(self) -> None:
        actual = assemble.parsetextlist('None', 'followupevents')

        assert actual == []

    def test_parse_text_list_raises_for_missing_value(self):

        with pytest.raises(ValueError, match="is missing"):
            assemble.parse_text_list(None, "commission_answer_text")

    def test_parsetextlist_raises_for_invalid_literal(self) -> None:
        with pytest.raises(ValueError, match='not a valid Python literal'):
            assemble.parsetextlist('[unclosed', 'commissionanswertext')

    def test_parse_text_list_raises_for_non_list_literal(self):

        raw = "'plain string'"

        with pytest.raises(ValueError, match="expected a list"):
            assemble.parse_text_list(raw, "commission_answer_text")


class TestConcatenateTextLists:
    def test_concatenate_text_lists_combines_answer_and_followup(self):

        responses_row = {
            "commission_answer_text": "['Answer 1', 'Answer 2']",
        }
        followup_row = {
            "followup_events": "['Follow-up 1']",
        }

        actual = assemble.concatenate_text_lists(responses_row, followup_row)

        assert actual == ["Answer 1", "Answer 2", "Follow-up 1"]

    def test_concatenate_text_lists_returns_only_answer_items_when_no_followup(self):

        responses_row = {
            "commission_answer_text": "['Answer 1']",
        }

        actual = assemble.concatenate_text_lists(responses_row, None)

        assert actual == ["Answer 1"]


class TestAssembleResults:
    def test_assemble_results_creates_one_analysis_input_per_response_row(
        self,
        monkeypatch,
        responses_rows,
        followup_rows,
    ):
        captured_calls: list[tuple[str, list[str]]] = []

        def fake_analyse_row(registration_number: str, text_items: list[str]) -> LegislationResult:

            captured_calls.append((registration_number, text_items))

            return LegislationResult(
                registration_number=registration_number,
                followup_events=text_items,
                Law_Passed=None,
                Is_Law_Passed=False,
                Rejected_Legislation=False,
            )

        monkeypatch.setattr(assemble, "analyse_row", fake_analyse_row)

        actual = assemble.assemble_results(responses_rows, followup_rows)

        assert len(actual) == 2
        assert captured_calls == [
            (
                "2012/000001",
                ["Commission answer 1", "Commission answer 2", "Follow-up 1", "Follow-up 2"],
            ),
            (
                "2012/000002",
                ["Commission answer 3", "Follow-up 3"],
            ),
        ]

    def test_assemble_results_handles_missing_followup_row(
        self,
        monkeypatch,
        responses_rows,
    ):

        captured_calls: list[tuple[str, list[str]]] = []

        def fake_analyse_row(registration_number: str, text_items: list[str]) -> LegislationResult:

            captured_calls.append((registration_number, text_items))
            
            return LegislationResult(
                registration_number=registration_number,
                followup_events=text_items,
            )

        monkeypatch.setattr(assemble, "analyse_row", fake_analyse_row)

        actual = assemble.assemble_results(responses_rows, [])

        assert len(actual) == 2
        assert captured_calls == [
            ("2012/000001", ["Commission answer 1", "Commission answer 2"]),
            ("2012/000002", ["Commission answer 3"]),
        ]

    def test_assemble_results_raises_for_empty_registration_number(
        self,
        monkeypatch,
        followup_rows,
    ):
        rows = [
            {
                "registration_number": "   ",
                "commission_answer_text": "['Answer 1']",
            }
        ]

        def fake_analyse_row(registration_number: str, text_items: list[str]) -> LegislationResult:
            raise AssertionError("analyse_row should not be called")

        monkeypatch.setattr(assemble, "analyse_row", fake_analyse_row)

        with pytest.raises(ValueError, match="empty registration_number"):
            assemble.assemble_results(rows, followup_rows)