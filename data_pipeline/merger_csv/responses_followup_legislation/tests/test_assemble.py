import pytest

from data_pipeline.merger_csv.responses_followup_legislation import assemble


class TestParseTextList:
    def test_parse_text_list_returns_items_for_valid_list_literal(self):

        raw = "['alpha', 'beta']"
        actual = assemble.parse_text_list(raw, "commission_answer_text")

        assert actual == ["alpha", "beta"]

    def test_parse_text_list_strips_whitespace_and_skips_empty_items(self):

        raw = "['  alpha  ', '', '   ', None, 'beta']"
        actual = assemble.parse_text_list(raw, "followup_events")
        
        assert actual == ["alpha", "beta"]

    def test_parse_text_list_returns_empty_list_for_literal_none(self) -> None:

        actual = assemble.parse_text_list('None', 'followup_events')
        
        assert actual == []

    def test_parse_text_list_raises_for_missing_value(self):

        with pytest.raises(ValueError, match="is missing"):
            assemble.parse_text_list(None, "commission_answer_text")

    def test_parse_text_list_raises_for_invalid_literal(self) -> None:

        with pytest.raises(ValueError, match='not a valid Python literal'):
            assemble.parse_text_list('[unclosed', 'commission_answer_text')

    def test_parse_text_list_raises_for_non_list_literal(self):

        with pytest.raises(ValueError, match="expected a list"):
            assemble.parse_text_list("'plain string'", "commission_answer_text")


class TestParseOptionalTextList:
    def test_parse_text_list_returns_empty_list_for_missing_value(self) -> None:

        assert assemble.parse_optional_text_list(None, 'followup_events') == []

    def test_parse_text_list_returns_empty_list_for_blank_string(self) -> None:

        assert assemble.parse_optional_text_list('   ', 'followup_events') == []

    def test_parse_text_list_parses_valid_list_literal(self) -> None:

        actual = assemble.parse_optional_text_list("['Follow-up 1']", 'followup_events')
        
        assert actual == ['Follow-up 1']


class TestMergeDeduplicateTextLists:
    def test_merge_deduplicated_text_lists_preserves_order_and_removes_duplicates(self) -> None:

        actual = assemble.merge_deduplicated_text_lists(
            ['Answer 1', 'Shared'],
            ['Embedded 1', 'Shared'],
            ['Separate 1', 'Embedded 1'],
        )
        
        assert actual == ['Answer 1', 'Shared', 'Embedded 1', 'Separate 1']


class TestConcatenateTextLists:
    def test_concatenate_text_lists_combines_answer_embedded_and_followup(self) -> None:

        responses_row = {
            'commission_answer_text': "['Answer 1', 'Answer 2']",
            'followup_events': "['Embedded follow-up 1']",
        }
        followup_row = {
            'followup_events': "['Separate follow-up 1', 'Separate follow-up 2']",
        }

        actual = assemble.concatenate_text_lists(responses_row, followup_row)

        assert actual == [
            'Answer 1',
            'Answer 2',
            'Embedded follow-up 1',
            'Separate follow-up 1',
            'Separate follow-up 2',
        ]

    def test_concatenate_text_lists_returns_only_answer_items_when_no_followup_exists(self) -> None:

        responses_row = {
            'commission_answer_text': "['Answer 1']",
        }

        actual = assemble.concatenate_text_lists(responses_row, None)

        assert actual == ['Answer 1']

    def test_concatenate_text_lists_includes_embedded_followup_without_separate_followup_row(self) -> None:

        responses_row = {
            'commission_answer_text': "['Answer 1']",
            'followup_events': "['Embedded follow-up 1']",
        }

        actual = assemble.concatenate_text_lists(responses_row, None)

        assert actual == ['Answer 1', 'Embedded follow-up 1']

    def test_concatenate_text_lists_deduplicates_across_both_followup_sources(self) -> None:

        responses_row = {
            'commission_answer_text': "['Answer 1']",
            'followup_events': "['Shared follow-up', 'Embedded only']",
        }
        followup_row = {
            'followup_events': "['Shared follow-up', 'Separate only']",
        }

        actual = assemble.concatenate_text_lists(responses_row, followup_row)

        assert actual == [
            'Answer 1',
            'Shared follow-up',
            'Embedded only',
            'Separate only',
        ]

    def test_concatenate_text_lists_raises_for_malformed_embedded_followup(self) -> None:

        responses_row = {
            'commission_answer_text': "['Answer 1']",
            'followup_events': '[unclosed',
        }

        with pytest.raises(ValueError, match='not a valid Python literal'):
            assemble.concatenate_text_lists(responses_row, None)


class TestAssembleResults:
    def test_assemble_results_creates_one_analysis_input_per_response_row(self, monkeypatch: pytest.MonkeyPatch) -> None:

        responses_rows = [
            {
                'registration_number': '2012/000001',
                'commission_answer_text': "['Commission answer 1', 'Commission answer 2']",
                'followup_events': "['Embedded follow-up 1']",
            },
            {
                'registration_number': '2012/000002',
                'commission_answer_text': "['Commission answer 3']",
            },
        ]

        followup_rows = [
            {
                'registration_number': '2012/000001',
                'followup_events': "['Embedded follow-up 1', 'Separate follow-up 1']",
            },
            {
                'registration_number': '2012/000002',
                'followup_events': "['Separate follow-up 2']",
            },
        ]

        captured_calls: list[tuple[str, list[str]]] = []

        def fake_analyse_row(registration_number: str, text_items: list[str]):

            captured_calls.append((registration_number, text_items))
            return {
                "registration_number": registration_number,
                "followup_events": text_items,
            }

        monkeypatch.setattr(assemble, 'analyse_row', fake_analyse_row)

        actual = assemble.assemble_results(responses_rows, followup_rows)

        assert len(actual) == 2
        assert captured_calls == [
            (
                '2012/000001',
                [
                    'Commission answer 1',
                    'Commission answer 2',
                    'Embedded follow-up 1',
                    'Separate follow-up 1',
                ],
            ),
            (
                '2012/000002',
                ['Commission answer 3', 'Separate follow-up 2'],
            ),
        ]

    def test_assemble_results_handles_missing_followup_row(self, monkeypatch: pytest.MonkeyPatch) -> None:

        responses_rows = [
            {
                'registration_number': '2012/000001',
                'commission_answer_text': "['Answer 1']",
                'followup_events': "['Embedded follow-up 1']",
            },
        ]
        
        captured_calls: list[tuple[str, list[str]]] = []

        def fake_analyse_row(registration_number: str, text_items: list[str]):

            captured_calls.append((registration_number, text_items))
            return {
                "registration_number": registration_number,
                "followup_events": text_items,
            }

        monkeypatch.setattr(assemble, 'analyse_row', fake_analyse_row)

        actual = assemble.assemble_results(responses_rows, [])

        assert len(actual) == 1
        assert captured_calls == [('2012/000001', ['Answer 1', 'Embedded follow-up 1'])]

    def test_assemble_results_raises_for_empty_registration_number(self, monkeypatch: pytest.MonkeyPatch) -> None:

        rows = [
            {
                'registration_number': '',
                'commission_answer_text': "['Answer 1']",
            },
        ]

        def fake_analyse_row(registration_number: str, text_items: list[str]):

            raise AssertionError('analyse_row should not be called')

        monkeypatch.setattr(assemble, 'analyse_row', fake_analyse_row)

        with pytest.raises(ValueError, match='empty registration_number'):
            assemble.assemble_results(rows, [])