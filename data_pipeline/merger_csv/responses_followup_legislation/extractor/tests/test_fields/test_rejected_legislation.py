import pytest

from data_pipeline.merger_csv.responses_followup_legislation.extractor.fields.rejected_legislation import (
    extract,
)


class TestExtractRejectedLegislationBulk:
    """
    Bulk tests if you forgot to write explicit one
    """

    def test_extract_returns_bool_for_all_samples(
        self,
        commission_answers_rejection_legislation,
    ) -> None:
        """
        Ensure the extractor always returns a strict boolean for every sample.
        """
        for (
            _,
            registration_number,
            text_items,
            _,
        ) in commission_answers_rejection_legislation:

            actual = extract(text_items)

            assert isinstance(actual, bool), (
                f"registration_number={registration_number}: expected bool, got "
                f"{type(actual).__name__}"
            )

    def test_extract_matches_expected_rejected_legislation_flags(
        self,
        commission_answers_rejection_legislation,
    ) -> None:
        """
        Verify that rejected_legislation.extract() matches the expected boolean
        outcome for each commission-answer sample defined in conftest.py.
        """
        for (
            expected,
            registration_number,
            text_items,
            rejection_statement,
        ) in commission_answers_rejection_legislation:

            actual = extract(text_items)

            assert actual is expected, (
                f"registration_number={registration_number}:\n"
                "expected `rejected_legislation`:\n"
                f"  {expected}\n"
                "got:\n"
                f"  {actual}\n"
                "text_item:\n"
                f"  {text_items}"
            )


class TestExtractRejectedLegislationExplicit:
    """
    Individual explicit tests to get visibility, what went wrong.
    """

    def _get_sample(
        self,
        commission_answers_rejection_legislation: list,
        registration_number: str,
    ) -> tuple:

        for sample in commission_answers_rejection_legislation:
            if sample[1] == registration_number:
                return sample

        raise KeyError(registration_number)

    def test_extract_returns_false_for_2012_000003(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2012/000003"
        )

        assert expected is False
        assert registration_number == "2012/000003"
        assert rejection_phrases is None
        assert extract(text_items) is False

    def test_extract_returns_true_for_2012_000005(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2012/000005"
        )

        assert expected is True
        assert registration_number == "2012/000005"
        assert rejection_phrases == ["not to submit a legislative proposal"]
        assert extract(text_items) is True

    def test_extract_returns_false_for_2017_000002(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2017/000002"
        )

        assert expected is False
        assert registration_number == "2017/000002"
        assert rejection_phrases == [
            "will not make a legislative proposal to that effect"
        ]  # It is canceled by proposition of other legislation
        assert extract(text_items) is False

    def test_extract_returns_true_for_2012_000007(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2012/000007"
        )

        assert expected is True
        assert registration_number == "2012/000007"
        assert rejection_phrases == ["no repeal of that legislation was proposed"]
        assert extract(text_items) is True

    def test_extract_returns_true_for_2017_000004(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2017/000004"
        )

        assert expected is True
        assert registration_number == "2017/000004"
        assert rejection_phrases == ["no further legal acts are proposed"]
        assert extract(text_items) is True

    def test_extract_returns_false_for_2018_000004(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2018/000004"
        )

        assert expected is False
        assert registration_number == "2018/000004"
        assert rejection_phrases is None
        assert extract(text_items) is False

    def test_extract_returns_true_for_2019_000007(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2019/000007"
        )

        assert expected is True
        assert registration_number == "2019/000007"
        assert rejection_phrases == ["no new legislation will be proposed "]
        assert extract(text_items) is True

    def test_extract_returns_false_for_2019_000016(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2019/000016"
        )

        assert expected is False
        assert registration_number == "2019/000016"
        assert rejection_phrases is None
        assert extract(text_items) is False

    def test_extract_returns_false_for_2020_000001(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2020/000001"
        )

        assert expected is False
        assert registration_number == "2020/000001"
        assert rejection_phrases is None
        assert extract(text_items) is False

    def test_extract_returns_false_for_2021_000006(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2021/000006"
        )

        assert expected is False
        assert registration_number == "2021/000006"
        assert rejection_phrases is None
        assert extract(text_items) is False

    def test_extract_returns_false_for_2022_000002(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2022/000002"
        )

        assert expected is False
        assert registration_number == "2022/000002"
        assert rejection_phrases is None
        assert extract(text_items) is False

    def test_extract_returns_true_for_2024_000004(
        self,
        commission_answers_rejection_legislation,
    ):

        expected, registration_number, text_items, rejection_phrases = self._get_sample(
            commission_answers_rejection_legislation, "2024/000004"
        )

        assert expected is True
        assert registration_number == "2024/000004"
        assert rejection_phrases == ["not necessary to propose a new legal instrument"]
        assert extract(text_items) is True
