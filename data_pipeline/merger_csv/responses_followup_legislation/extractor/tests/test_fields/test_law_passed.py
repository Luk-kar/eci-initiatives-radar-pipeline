import pytest

from data_pipeline.merger_csv.responses_followup_legislation.extractor.fields.law_passed import (
    extract,
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
        Verify that law_passed.extract() matches the expected list of sentences
        for each followup-event sample defined in conftest.py.
        """
        for row in followup_events_law_passed:
            if len(row) < 3:
                continue

            registration_number, expected, text_items = row

            actual = extract(text_items)

            assert actual == expected, (
                f"registration_number={registration_number}:\n"
                "expected `law_passed` sentences:\n"
                f"  {expected}\n"
                "got:\n"
                f"  {actual}\n"
                "input text_items:\n"
                f"  {text_items}"
            )

class TestExtractLawPassedExplicit:
    """
    Tests for explicit law-passed extraction, one test per ECI registration number,
    driven by the ``followup_events_law_passed`` fixture.
    """

    def test_2012_000003(self, followup_events_law_passed):
        registration, expected_sentences, source = followup_events_law_passed[0]
        assert registration == "2012/000003"

        result = extract(source)
        combined_source_string = "\n".join(result)
        for sentence in expected_sentences:
            assert sentence in combined_source_string

        assert (len(expected_sentences)) == len(result)

    def test_2012_000005(self, followup_events_law_passed):
        registration, expected, source = followup_events_law_passed[1]
        assert registration == "2012/000005"
        result = extract(source)
        assert result is None

    def test_2017_000002(self, followup_events_law_passed):
        registration, expected, source = followup_events_law_passed[2]
        assert registration == "2017/000002"
        result = extract(source)
        assert result == expected

    def test_2012_000007(self, followup_events_law_passed):
        registration, expected, source = followup_events_law_passed[3]
        assert registration == "2012/000007"
        result = extract(source)
        assert result is None

    def test_2017_000004(self, followup_events_law_passed):
        registration, expected, source = followup_events_law_passed[4]
        assert registration == "2017/000004"
        result = extract(source)
        assert result is None

    def test_2018_000004(self, followup_events_law_passed):
        registration, expected, source = followup_events_law_passed[5]
        assert registration == "2018/000004"
        result = extract(source)
        assert result is None

    def test_2019_000016(self, followup_events_law_passed):
        registration, expected, source = followup_events_law_passed[6]
        assert registration == "2019/000016"
        result = extract(source)
        assert result == expected

    def test_2020_000001(self, followup_events_law_passed):
        registration, expected, source = followup_events_law_passed[7]
        assert registration == "2020/000001"
        result = extract(source)
        assert result == expected

    def test_2021_000006(self, followup_events_law_passed):
        registration, expected, source = followup_events_law_passed[8]
        assert registration == "2021/000006"
        result = extract(source)
        assert result is None

    def test_2022_000002(self, followup_events_law_passed):
        registration, expected, source = followup_events_law_passed[9]
        assert registration == "2022/000002"
        result = extract(source)
        assert result == expected

    def test_2024_000004(self, followup_events_law_passed):
        registration, expected, source = followup_events_law_passed[10]
        assert registration == "2024/000004"
        result = extract(source)
        assert result is None