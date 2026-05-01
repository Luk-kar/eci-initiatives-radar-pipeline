import pytest

from data_pipeline.merger_csv.responses_followup_legislation.extractor.fields.is_law_passed import (
    extract,
)


class TestIsLawPassed:
    """
    Tests for the derivation logic of ``Is_Law_Passed`` from ``law_passed``.
    """

    @pytest.mark.parametrize(
        "law_passed_input, expected_result",
        [
            # True cases: The list contains at least one valid, non-empty string
            (["The directive was adopted."], True),
            ([""], False),  # Sanity check on the empty string below
            (["   ", "The directive was adopted.", None], True),
            (
                [
                    "The Commission adopted the regulation.",
                    "It entered into force in 2020.",
                ],
                True,
            ),
            # False cases: None, empty lists, or lists containing only empty/whitespace/None values
            (None, False),
            ([], False),
            ([""], False),
            (["   "], False),
            (["\n\t"], False),
            ([None], False),
            ([None, "", "  "], False),
        ],
    )
    def test_extract_derives_correct_boolean(
        self, law_passed_input: list[str] | None, expected_result: bool
    ):
        """
        Verify that `extract` returns True only when the input list contains
        at least one valid, non-empty string.
        """

        actual_result = extract(law_passed_input)

        assert actual_result is expected_result, (
            f"Failed for input: {law_passed_input}. "
            f"Expected {expected_result}, got {actual_result}."
        )

    def test_extract_preserves_boolean_type(self):
        """
        Ensure the return type is explicitly a boolean, not a truthy/falsy value.
        """
        assert isinstance(extract(["Test string"]), bool)
        assert isinstance(extract(None), bool)
        assert isinstance(extract([]), bool)
