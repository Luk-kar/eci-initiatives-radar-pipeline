"""
Tests for ``data_pipeline.merger_csv.dashboard_csv.extractor.fields.registration_year``.

Covered behaviour:
  * Standard year extraction from valid registration numbers.
  * Empty / None registration numbers raise an error.
  * Registration numbers without a "/" raise an error
  * Multiple "/" characters raise an error.
  * Raise an error when registration number do not follow pattern
"""

import pytest

from data_pipeline.merger_csv.dashboard_csv.extractor.fields.registration_year import (
    extract,
)


class TestExtractValid:
    """Tests for standard valid extraction."""

    @pytest.mark.parametrize(
        "registration_number, expected",
        [
            ("2012/000001", "2012"),
            ("2024/000012", "2024"),
            ("1999/123456", "1999"),
        ],
    )
    def test_valid_extraction(self, registration_number: str, expected: str) -> None:
        """The year prefix is successfully extracted."""
        assert extract(registration_number) == expected


class TestExtractErrors:
    """Tests for malformed or missing registration numbers."""

    @pytest.mark.parametrize(
        "empty_val",
        [
            None,
            "",
            "   ",
            "\n",
        ],
    )
    def test_empty_or_none_raises_error(self, empty_val: str | None) -> None:
        """Empty / None registration numbers raise an error."""
        with pytest.raises(
            ValueError, match="Registration number cannot be empty or None"
        ):
            extract(empty_val)

    @pytest.mark.parametrize(
        "no_slash",
        [
            "2012-000001",
            "2012000001",
            "just_a_string",
        ],
    )
    def test_no_slash_raises_error(self, no_slash: str) -> None:
        """Registration numbers without a '/' raise an error."""

        with pytest.raises(ValueError, match="Registration number must contain a '/'"):
            extract(no_slash)

    @pytest.mark.parametrize(
        "multi_slash",
        [
            "2012/001/01",
            "2023/12/34/56",
            "2024//000001",
        ],
    )
    def test_multiple_slashes_raises_error(self, multi_slash: str) -> None:
        """Multiple '/' characters raise an error."""
        with pytest.raises(
            ValueError, match="Registration number must contain exactly one '/'"
        ):
            extract(multi_slash)

    @pytest.mark.parametrize(
        "bad_pattern",
        [
            "123/000001",  # Year is only 3 digits
            "2024A/000001",  # Year contains letters
            "2024/ABCDEF",  # Suffix contains letters
            "20/24/000001",  # Split incorrectly
            "2024/ 000001",  # Contains space
        ],
    )
    def test_bad_pattern_raises_error(self, bad_pattern: str) -> None:
        """Raise an error when registration number does not follow the YYYY/NNNNNN pattern."""

        # Using a general match because `multi_slash` case could trigger earlier for "20/24/000001"
        with pytest.raises(ValueError):
            extract(bad_pattern)

    def test_exact_pattern_error_message(self) -> None:
        """Ensure the specific pattern error message is raised for non-numeric components."""

        with pytest.raises(ValueError, match="does not follow the expected pattern"):
            extract("202A/00001")
