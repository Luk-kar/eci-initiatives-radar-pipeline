import pytest

from data_pipeline.merger_csv.responses_followup_legislation.extractor.fields.rejected_legislation import (
    extract,
)


def test_extract_returns_bool_for_all_samples(
    commission_answers_rejection_legislation,
) -> None:
    """
    Ensure the extractor always returns a strict boolean for every sample.
    """
    for _, registration_number, text_items in commission_answers_rejection_legislation:

        actual = extract(text_items)

        assert isinstance(actual, bool), (
            f"registration_number={registration_number}: expected bool, got "
            f"{type(actual).__name__}"
        )


def test_extract_matches_expected_rejected_legislation_flags(
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
