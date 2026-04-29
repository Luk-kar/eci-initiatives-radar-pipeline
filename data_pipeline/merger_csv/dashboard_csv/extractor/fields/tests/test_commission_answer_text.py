"""
Tests for ``data_pipeline.merger_csv.dashboard_csv.extractor.fields.commission_answer_text``.

Covered behaviour:
  * None / empty string / whitespace normalisation.
  * Robust literal parsing (SyntaxError, ValueError).
  * Type enforcement (ignoring non-list literals).
  * Filtering of empty paragraphs, whitespace-only paragraphs, and non-strings.
  * Correct joining of multiple paragraphs.
"""

import logging

import pytest

from data_pipeline.merger_csv.dashboard_csv.extractor.fields.commission_answer_text import (
    _summarise,
    extract,
)


class TestExtractCore:
    """Tests for the main extract() entry point and literal parsing logic."""

    @pytest.mark.parametrize(
        "raw_cell",
        [
            None,
            "",
            "   ",
            "\n\t",
        ],
    )
    def test_empty_or_none(self, raw_cell: str | None) -> None:
        """Empty, whitespace-only, and None values return an empty string."""
        assert extract(raw_cell) == ""

    @pytest.mark.parametrize(
        "invalid_literal",
        [
            "[this is not valid python]",
            "['unclosed list",
            "{malformed dict",
        ],
    )
    def test_invalid_literal(
        self, invalid_literal: str, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Syntax and ValueError during parsing are caught, logged, and return an empty string."""
        with caplog.at_level(logging.WARNING):
            result = extract(invalid_literal)

        assert result == ""
        assert "Failed to parse commission_answer_text literal" in caplog.text

    @pytest.mark.parametrize(
        "valid_but_not_list",
        [
            "'Just a string'",
            "42",
            "{'a': 1}",
            "('tuple',)",
        ],
    )
    def test_not_a_list(
        self, valid_but_not_list: str, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Valid Python literals that are not lists log a warning and return an empty string."""
        with caplog.at_level(logging.WARNING):
            result = extract(valid_but_not_list)

        assert result == ""
        assert "Expected commission_answer_text to parse into a list" in caplog.text

    def test_valid_list(self) -> None:
        """A valid stringified list of paragraphs is parsed and joined."""
        raw = "['First paragraph.', 'Second paragraph.']"
        assert extract(raw) == "First paragraph.\nSecond paragraph."


class TestSummarise:
    """Tests for the text filtering and summarisation logic."""

    def test_filters_empty_and_whitespace(self) -> None:
        """Empty strings and whitespace-only strings are ignored."""
        paragraphs = ["First.", "", "   ", "\n", "Second."]
        assert _summarise(paragraphs) == "First.\nSecond."

    def test_filters_non_strings(self) -> None:
        """Non-string elements in the parsed list are safely ignored."""
        # Using type: ignore because we are deliberately testing runtime safety
        # against dirty data that bypassed the type checker.
        paragraphs = ["First.", 42, None, ["nested"], "Second."]  # type: ignore
        assert _summarise(paragraphs) == "First.\nSecond."

    def test_strips_paragraphs(self) -> None:
        """Leading and trailing whitespace on individual paragraphs is stripped."""
        paragraphs = ["  First.  ", "\tSecond.\n"]
        assert _summarise(paragraphs) == "First.\nSecond."


class TestIntegration:
    """Tests for the end-to-end extraction with real-world data payloads."""

    def test_real_world_example(self) -> None:
        """Ensure a large, real-world stringified list parses and cleans correctly."""
        raw = (
            "['The Commission committed, in particular, to taking the following actions:', "
            "'reinforcing implementation of EU water quality legislation...', ]"
        )
        expected = (
            "The Commission committed, in particular, to taking the following actions:\n"
            "reinforcing implementation of EU water quality legislation..."
        )
        assert extract(raw) == expected
