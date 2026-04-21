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

        for (
            registration_number,
            _,
            text_items,
        ) in followup_events_law_passed:

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

        for (
            registration_number,
            expected,
            text_items,
        ) in followup_events_law_passed:
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
    Individual explicit tests to verify specific ECI behavior and get visibility
    into what went wrong if parsing fails for a specific initiative.
    """

    def _get_sample(
        self,
        followup_events_law_passed: list,
        registration_number: str,
    ) -> tuple:

        for sample in followup_events_law_passed:
            if sample[0] == registration_number:
                return sample

        raise KeyError(registration_number)

    def test_extract_returns_expected_for_2012_000003(
        self,
        followup_events_law_passed,
    ):

        registration_number, expected, text_items = self._get_sample(
            followup_events_law_passed, "2012/000003"
        )
        assert registration_number == "2012/000003"
        assert extract(text_items) == expected
        assert (
            len(expected) == 9
        )  # Sanity check: verify multiple sentences were matched

    def test_extract_returns_none_for_2012_000005(
        self,
        followup_events_law_passed,
    ):

        # 2012/000005 'One of Us' had no new law passed
        registration_number, expected, text_items = self._get_sample(
            followup_events_law_passed, "2012/000005"
        )
        assert registration_number == "2012/000005"
        assert expected is None
        assert extract(text_items) is None

    def test_extract_returns_expected_for_2017_000002(
        self,
        followup_events_law_passed,
    ):

        registration_number, expected, text_items = self._get_sample(
            followup_events_law_passed, "2017/000002"
        )
        assert registration_number == "2017/000002"
        assert expected is not None
        assert extract(text_items) == expected

    def test_extract_returns_none_for_2017_000004(
        self,
        followup_events_law_passed,
    ):

        # Minority SafePack - No new law entered into force from the follow-up
        registration_number, expected, text_items = self._get_sample(
            followup_events_law_passed, "2017/000004"
        )
        assert registration_number == "2017/000004"
        assert expected is None
        assert extract(text_items) is None

    def test_extract_returns_expected_for_2019_000016(
        self,
        followup_events_law_passed,
    ):

        registration_number, expected, text_items = self._get_sample(
            followup_events_law_passed, "2019/000016"
        )
        assert registration_number == "2019/000016"
        assert expected is not None
        assert "entered into force on 18 August 2024" in expected[1]
        assert extract(text_items) == expected

    def test_extract_returns_expected_for_2020_000001(
        self,
        followup_events_law_passed,
    ):

        registration_number, expected, text_items = self._get_sample(
            followup_events_law_passed, "2020/000001"
        )
        assert registration_number == "2020/000001"
        assert expected is not None
        assert any("entered into force in January 2024" in e for e in expected)
        assert extract(text_items) == expected

    def test_extract_returns_none_for_2021_000006(
        self,
        followup_events_law_passed,
    ):

        # Save Cruelty Free Cosmetics - Roadmap work ongoing, no laws passed yet
        registration_number, expected, text_items = self._get_sample(
            followup_events_law_passed, "2021/000006"
        )
        assert registration_number == "2021/000006"
        assert expected is None
        assert extract(text_items) is None

    def test_extract_handles_none_input(self):
        """
        Verify that if the ECI has absolutely no followup_events (None input),
        the extractor handles it gracefully and returns None.
        """

        assert extract(None) is None
