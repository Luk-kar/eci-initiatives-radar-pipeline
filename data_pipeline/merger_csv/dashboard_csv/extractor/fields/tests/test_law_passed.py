"""
Tests for ``data_pipeline.merger_csv.dashboard_csv.extractor.fields.law_passed``.

Covered behaviour:
  * Empty / None normalisation (returns "").
  * Invalid literals raise ValueError.
  * Non-list parsed types raise TypeError.
  * Markdown links are flattened to their anchor text.
  * Non-string elements inside the parsed list are ignored.
  * Empty / whitespace-only paragraphs are skipped.
  * Valid paragraphs are stripped and joined by newlines.
"""

import pytest

from data_pipeline.merger_csv.dashboard_csv.extractor.fields.law_passed import (
    _flatten_markdown_links,
    extract,
)


class TestCoreExtraction:
    """Tests for empty handling and basic valid extractions."""

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


class TestErrorHandling:
    """Tests to enforce strict literal parsing and type safety."""

    @pytest.mark.parametrize(
        "invalid_literal",
        [
            "[this is not valid python]",
            "['unclosed list",
            "{malformed dict",
        ],
    )
    def test_parsing_raises_value_error(self, invalid_literal: str) -> None:
        """Syntax and ValueError during parsing raise a descriptive ValueError."""
        with pytest.raises(ValueError, match="Failed to parse law_passed literal"):
            extract(invalid_literal)

    @pytest.mark.parametrize(
        "valid_but_not_list",
        [
            "'Just a string'",
            "42",
            "{'a': 1}",
            "('tuple',)",
        ],
    )
    def test_parsing_raises_type_error(self, valid_but_not_list: str) -> None:
        """Valid Python literals that are not lists raise a TypeError."""
        with pytest.raises(TypeError, match="Expected law_passed to parse into a list"):
            extract(valid_but_not_list)


class TestParagraphProcessing:
    """Tests for markdown stripping, filtering, and joining logic."""

    @pytest.mark.parametrize(
        "raw_text, expected",
        [
            ("No links here.", "No links here."),
            (
                "Read the [Directive](http://example.com) now.",
                "Read the Directive now.",
            ),
            ("[Link 1](url1) and [Link 2](url2).", "Link 1 and Link 2."),
            (
                "See [press release](http://europa.eu/rapid/..._en.htm) today.",
                "See press release today.",
            ),
        ],
    )
    def test_flatten_markdown_links(self, raw_text: str, expected: str) -> None:
        """Markdown links are correctly replaced by their display text."""
        assert _flatten_markdown_links(raw_text) == expected

    def test_joins_with_newline(self) -> None:
        """Multiple paragraphs are joined by a single newline character."""
        raw = "['First paragraph.', 'Second paragraph.']"
        assert extract(raw) == "First paragraph.\nSecond paragraph."

    def test_skips_non_strings_and_empty(self) -> None:
        """Non-strings and empty or whitespace-only strings are ignored."""
        raw = "['First.', 42, None, '', '   ', 'Second.']"
        assert extract(raw) == "First.\nSecond."

    def test_strips_paragraphs(self) -> None:
        """Surrounding whitespace is stripped from paragraphs before joining."""
        raw = "['  First paragraph.  ', '\\tSecond paragraph.\\n']"
        assert extract(raw) == "First paragraph.\nSecond paragraph."


class TestIntegration:
    """Tests verifying behavior against data structures seen in the wild."""

    def test_real_world_example(self) -> None:
        """Test a complex real-world list of markdown-heavy paragraphs."""
        raw = (
            '["Amendment to the [Drinking Water Directive](http://eur-lex.europa.eu/...) '
            'came into force (see [press release](http://europa.eu/..._en.htm) ).", '
            "'A [proposal for a regulation on minimum requirements](https://ec.europa.eu/...pdf) "
            "was adopted in May 2018.']"
        )
        expected = (
            "Amendment to the Drinking Water Directive came into force (see press release ).\n"
            "A proposal for a regulation on minimum requirements was adopted in May 2018."
        )
        assert extract(raw) == expected
