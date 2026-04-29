"""
Tests for ``data_pipeline.merger_csv.dashboard_csv.extractor.fields.signatures_collected_by_country``.

Covered behaviour:
  * Empty / None values return an empty string.
  * Valid strings (Python dict literals) are parsed and serialized to JSON.
  * Thousands comma formatting for signatures and thresholds.
  * Percentage symbol appending for percentages.
  * Robust literal parsing raises ValueError on syntax/parsing errors.
  * Strict type checking raises TypeError for non-dictionary structures.
  * Invalid nested numbers (e.g. string letters) raise ValueError during conversion.
"""

import json
import pytest

from data_pipeline.merger_csv.dashboard_csv.extractor.fields.signatures_collected_by_country import (
    extract,
)


class TestCoreExtraction:
    """Tests for empty handling and end-to-end valid extraction."""

    @pytest.mark.parametrize(
        "raw",
        [
            None,
            "",
            "   ",
            "\n\t",
        ],
    )
    def test_empty_or_none(self, raw: str | None) -> None:
        """Empty strings, whitespace, and None immediately return an empty string."""

        assert extract(raw) == ""

    def test_valid_json_serialization(self) -> None:
        """The output string is a valid JSON string (double quotes, not single quotes)."""

        raw = "{'Austria': {'signatures': 24973, 'threshold': 14250, 'percentage': 175.25}}"
        result = extract(raw)

        # Will raise json.JSONDecodeError if invalid JSON
        parsed_result = json.loads(result)

        assert "Austria" in parsed_result
        assert parsed_result["Austria"]["signatures"] == "24,973"


class TestFormattingRules:
    """Tests to verify numeric values are correctly formatted as strings."""

    def test_comma_formatting(self) -> None:
        """Signatures and thresholds are formatted with commas separating thousands."""
        raw = "{'Germany': {'signatures': 137874, 'threshold': 74250}}"
        result = extract(raw)
        parsed = json.loads(result)

        assert parsed["Germany"]["signatures"] == "137,874"
        assert parsed["Germany"]["threshold"] == "74,250"

    def test_percentage_formatting(self) -> None:
        """Percentage values have a '%' appended and retain their numeric identity."""
        raw = "{'Italy': {'percentage': 1139.63}, 'Sweden': {'percentage': 16.45}}"
        result = extract(raw)
        parsed = json.loads(result)

        assert parsed["Italy"]["percentage"] == "1139.63%"
        assert parsed["Sweden"]["percentage"] == "16.45%"

    def test_missing_nested_keys(self) -> None:
        """Missing inner keys are safely omitted from the country's output."""
        raw = "{'Poland': {'signatures': 235964}}"
        result = extract(raw)
        parsed = json.loads(result)

        assert parsed["Poland"]["signatures"] == "235,964"
        assert "threshold" not in parsed["Poland"]
        assert "percentage" not in parsed["Poland"]


class TestErrorHandling:
    """Tests verifying that exceptions are strictly raised on malformed data."""

    @pytest.mark.parametrize(
        "invalid_literal",
        [
            "{'Austria':",  # Unclosed dict
            "just string data",  # Invalid syntax
            "{malformed key: 1}",  # Unquoted key
        ],
    )
    def test_parsing_raises_value_error(self, invalid_literal: str) -> None:
        """Syntax and ValueErrors during AST evaluation raise a ValueError."""

        with pytest.raises(
            ValueError, match="Failed to parse signatures_collected_by_country literal"
        ):
            extract(invalid_literal)

    @pytest.mark.parametrize(
        "valid_but_not_dict",
        [
            "['just a list']",
            "'just a string'",
            "42",
        ],
    )
    def test_parsing_raises_type_error_for_non_dict(
        self, valid_but_not_dict: str
    ) -> None:
        """Valid Python literals that are not dictionaries raise a TypeError."""

        with pytest.raises(
            TypeError,
            match="Expected signatures_collected_by_country to parse into a dict",
        ):
            extract(valid_but_not_dict)

    def test_nested_non_dict_raises_type_error(self) -> None:
        """A country key pointing to a non-dict raises a TypeError."""

        raw = "{'France': 83503}"
        with pytest.raises(
            TypeError, match="Expected stats for country 'France' to be a dict"
        ):
            extract(raw)

    @pytest.mark.parametrize(
        "bad_signatures",
        [
            "{'Austria': {'signatures': 'not-a-number'}}",
            "{'Austria': {'signatures': [1, 2, 3]}}",
        ],
    )
    def test_invalid_signatures_value_raises(self, bad_signatures: str) -> None:
        """Non-numeric values for signatures raise a ValueError during integer conversion."""

        with pytest.raises(ValueError, match="Invalid signatures value for 'Austria'"):
            extract(bad_signatures)

    @pytest.mark.parametrize(
        "bad_threshold",
        [
            "{'Belgium': {'threshold': 'TBD'}}",
            "{'Belgium': {'threshold': {'data': 16500}}}",
        ],
    )
    def test_invalid_threshold_value_raises(self, bad_threshold: str) -> None:
        """Non-numeric values for threshold raise a ValueError during integer conversion."""

        with pytest.raises(ValueError, match="Invalid threshold value for 'Belgium'"):
            extract(bad_threshold)

    @pytest.mark.parametrize(
        "bad_percentage",
        [
            "{'Bulgaria': {'percentage': 'unknown'}}",
            "{'Bulgaria': {'percentage': None}}",
        ],
    )
    def test_invalid_percentage_value_raises(self, bad_percentage: str) -> None:
        """Non-numeric values for percentage raise a ValueError during float conversion."""

        with pytest.raises(ValueError, match="Invalid percentage value for 'Bulgaria'"):
            extract(bad_percentage)
