import pytest

from data_pipeline.merger_csv.responses_followup_legislation.extractor.fields.law_passed import (
    extract,_split_into_sentences
)

class TestExtractLawPassedBulk:
    """
    Bulk tests to ensure robust behavior across all expected ECI responses.
    """

    def test_extract_returns_list_of_strings_or_none_for_all_samples(
        self,
        followup_events_law_passed,
    ) -> None:
        """
        Ensure the extractor always returns a list of strings or None for every sample.
        """
        for row in followup_events_law_passed:
            if len(row) < 3:
                continue

            registration_number, _, text_items = row

            actual = extract(text_items)

            if actual is not None:
                assert isinstance(actual, list), (
                    f"registration_number={registration_number}: expected list or None, got "
                    f"{type(actual).__name__}"
                )

                for item in actual:
                    assert isinstance(item, str), (
                        f"registration_number={registration_number}: expected string in list, got "
                        f"{type(item).__name__}"
                    )

    def test_extract_matches_expected_law_passed_sentences(
        self,
        followup_events_law_passed,
    ) -> None:
        """
        Verify that law_passed.extract() captures all expected sentences
        and does not capture unexpected items for each followup-event sample.
        """
        for row in followup_events_law_passed:
            if len(row) < 3:
                continue

            registration_number, expected, text_items = row

            actual = extract(text_items)

            if not expected:
                assert not actual, (
                    f"registration_number={registration_number}:\n"
                    f"Expected no results, but got:\n{actual}"
                )
                continue

            assert actual is not None, (
                f"registration_number={registration_number}:\n"
                f"Expected {len(expected)} sentences, but extract() returned None"
            )

            combined_source_string = "\n".join(actual)

            # Verify that all expected sentences were captured
            for sentence in expected:
                assert sentence in combined_source_string, (
                    f"registration_number={registration_number}:\n"
                    f"Missing expected sentence:\n  {sentence}\n\n"
                    f"In combined output:\n  {combined_source_string}"
                )

            # Verify that no extra/false-positive sentences were captured
            assert len(expected) == len(actual), (
                f"registration_number={registration_number}:\n"
                f"Expected {len(expected)} results, got {len(actual)}.\n"
                f"Expected:\n  {expected}\n"
                f"Got:\n  {actual}"
            )

class TestExtractLawPassedExplicit:
    """
    Tests for explicit law-passed extraction, one test per ECI registration number,
    driven by the ``followup_events_law_passed`` fixture.
    """

    def _assert_extraction(self, expected_registration: str, test_data: tuple):
        """
        Common assertion logic to validate the extracted law-passed text.
        """
        registration, expected_sentences, source = test_data
        
        # Ensure the test is checking the correct registration data
        assert registration == expected_registration
        
        result = extract(source)
        
        # Handle cases where no extraction is expected
        if not expected_sentences:
            assert not result, f"Expected no results, but got {result}"
            return

        assert result is not None, f"Expected {len(expected_sentences)} sentences, but extract() returned None"
        
        combined_source_string = "\n".join(result)
        
        # Verify that all expected sentences were captured
        for sentence in expected_sentences:
            assert sentence in combined_source_string

        # Verify that no extra/false-positive sentences were captured
        assert len(expected_sentences) == len(result), (
            f"Expected {len(expected_sentences)} results, got {len(result)}"
        )

    def test_2012_000003(self, followup_events_law_passed):
        self._assert_extraction("2012/000003", followup_events_law_passed[0])

    def test_2012_000005(self, followup_events_law_passed):
        self._assert_extraction("2012/000005", followup_events_law_passed[1])

    def test_2017_000002(self, followup_events_law_passed):
        self._assert_extraction("2017/000002", followup_events_law_passed[2])

    def test_2012_000007(self, followup_events_law_passed):
        self._assert_extraction("2012/000007", followup_events_law_passed[3])

    def test_2017_000004(self, followup_events_law_passed):
        self._assert_extraction("2017/000004", followup_events_law_passed[4])

    def test_2018_000004(self, followup_events_law_passed):
        self._assert_extraction("2018/000004", followup_events_law_passed[5])

    def test_2019_000016(self, followup_events_law_passed):
        self._assert_extraction("2019/000016", followup_events_law_passed[6])

    def test_2020_000001(self, followup_events_law_passed):
        self._assert_extraction("2020/000001", followup_events_law_passed[7])

    def test_2021_000006(self, followup_events_law_passed):
        self._assert_extraction("2021/000006", followup_events_law_passed[8])

    def test_2022_000002(self, followup_events_law_passed):
        self._assert_extraction("2022/000002", followup_events_law_passed[9])

    def test_2024_000004(self, followup_events_law_passed):
        self._assert_extraction("2024/000004", followup_events_law_passed[10])


class TestSplitIntoSentences:
    
    @pytest.mark.parametrize(
        "input_text, expected_chunks",
        [
            # 1. The specific 'i.e.' case from the prompt
            (
                "The Regulation was published in the Official Journal of the EU on 6 September 2019. Following its entry into force 20 days after publication, it became applicable 18 months later, i.e. on 27 March 2021 .",
                [
                    "The Regulation was published in the Official Journal of the EU on 6 September 2019.",
                    "Following its entry into force 20 days after publication, it became applicable 18 months later, i.e. on 27 March 2021 ."
                ]
            ),
            # 2. Standard sentence splitting with multiple punctuation types
            (
                "First sentence. Second sentence! Third sentence?",
                [
                    "First sentence.",
                    "Second sentence!",
                    "Third sentence?"
                ]
            ),
            # 3. Handling 'e.g.'
            (
                "This applies to many things, e.g. water and air. We need them to survive.",
                [
                    "This applies to many things, e.g. water and air.",
                    "We need them to survive."
                ]
            ),
            # 4. Handling 'etc.'
            (
                "They bought apples, bananas, etc. at the market. Then they went home.",
                [
                    "They bought apples, bananas, etc. at the market.",
                    "Then they went home."
                ]
            ),
            # 5. Empty or whitespace-only strings
            (
                "   ",
                []
            )
        ]
    )
    def test_abbreviation_handling(self, input_text: str, expected_chunks: list[str]):
        """
        Ensures text is split on terminal punctuation (.!?) but ignores periods 
        inside common abbreviations like i.e., e.g., and etc.
        """
        result = _split_into_sentences(input_text)
        assert result == expected_chunks

class TestExtractLawPassedRejectedLegislationArgument:
    """
    Tests the early-exit behavior of the `rejected_legislation` argument.
    """

    def test_returns_none_when_rejected_legislation_is_true(self) -> None:
        """
        Ensure that if rejected_legislation=True, the extractor completely 
        bypasses the regex search and returns None, even with matching text.
        """
        text_items = [
            "The Regulation entered into force in January 2020.",
            "The Commission adopted the directive."
        ]
        
        result = extract(text_items, rejected_legislation=True)
        
        assert result is None, "Expected None when rejected_legislation is True"

    def test_processes_normally_when_rejected_legislation_is_false(self) -> None:
        """
        Ensure that if rejected_legislation=False (the default), the extractor 
        processes the text items and returns matches normally.
        """
        text_items = [
            "The Regulation entered into force in January 2020."
        ]
        
        result = extract(text_items, rejected_legislation=False)
        
        assert result is not None
        assert len(result) == 1
        assert result[0] == "The Regulation entered into force in January 2020."

    def test_handles_empty_text_items_safely(self) -> None:
        """
        Ensure that empty text items return None safely regardless of the flag.
        """
        assert extract([], rejected_legislation=True) is None
        assert extract([], rejected_legislation=False) is None