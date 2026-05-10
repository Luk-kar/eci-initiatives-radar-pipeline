"""Tests for datapipeline.mergercsv.dashboardcsv.extractor.fields.law_passed.

Covered behaviour:
- Empty/None normalisation returns [].
- Invalid literals raise ValueError.
- Non-list parsed types raise TypeError.
- Markdown links are flattened to their anchor text.
- Non-string elements inside the parsed list are ignored.
- Empty/whitespace-only paragraphs are skipped.
- Valid paragraphs are stripped and returned as individual list items.
"""

import pytest
from data_pipeline.merger_csv.dashboard_csv.extractor.fields.law_passed import (
    flatten_markdown_links,
    extract,
)


class TestCoreExtraction:
    """Tests for empty handling and basic valid extractions."""

    @pytest.mark.parametrize("raw", [None, "", "   ", "  \n  "])
    def test_empty_or_none(self, raw: str | None) -> None:
        """Empty strings, whitespace, and None immediately return an empty string."""
        assert extract(raw) == None


class TestErrorHandling:
    """Tests to enforce strict literal parsing and type safety."""

    @pytest.mark.parametrize(
        "invalid_literal",
        ["this is not valid python", "['unclosed list", "{'malformed': dict}"],
    )
    def test_parsing_raises_value_error(self, invalid_literal: str) -> None:
        """Syntax and ValueError during parsing raise a descriptive ValueError."""
        with pytest.raises(ValueError, match="Failed to parse law_passed literal"):
            extract(invalid_literal)

    @pytest.mark.parametrize(
        "valid_but_not_list",
        ["'Just a string'", "42", "{'a': 1}", "(1, 2)"],
    )
    def test_parsing_raises_type_error(self, valid_but_not_list: str) -> None:
        """Valid Python literals that are not lists raise a TypeError."""
        with pytest.raises(TypeError, match="Expected law_passed to parse into a list"):
            extract(valid_but_not_list)


class TestParagraphProcessing:
    """Tests for markdown stripping, filtering, and return structure."""

    @pytest.mark.parametrize(
        "raw_text, expected",
        [
            ("No links here.", "No links here."),
            (
                "[Read the Directive](http://example.com) now.",
                "Read the Directive now.",
            ),
            ("[Link 1](url1) and [Link 2](url2).", "Link 1 and Link 2."),
            ("See [press release](http://x.com) today.", "See press release today."),
        ],
    )
    def test_flatten_markdown_links(self, raw_text: str, expected: str) -> None:
        """Markdown links are correctly replaced by their display text."""
        assert flatten_markdown_links(raw_text) == expected

    def test_returns_list_of_strings(self) -> None:
        """extract() always returns a list."""
        raw = "['First paragraph.', 'Second paragraph.']"
        result = extract(raw)
        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)

    def test_each_paragraph_is_separate_item(self) -> None:
        """Multiple paragraphs are returned as separate list items."""
        raw = "['First paragraph.', 'Second paragraph.']"
        result = extract(raw)
        assert result == ["First paragraph.", "Second paragraph."]

    def test_skips_non_strings_and_empty(self) -> None:
        """Non-strings and empty or whitespace-only strings are ignored."""
        raw = "['First.', 42, None, '', '   ', 'Second.']"
        assert extract(raw) == ["First.", "Second."]

    def test_strips_paragraphs(self) -> None:
        """Surrounding whitespace is stripped from each paragraph."""
        raw = "['  First paragraph.  ', '  Second paragraph.  ']"
        assert extract(raw) == ["First paragraph.", "Second paragraph."]

    def test_single_paragraph_returns_single_item_list(self) -> None:
        """A single-element list returns a list with one item."""
        raw = "['Only entry.']"
        assert extract(raw) == ["Only entry."]


class TestIntegration:
    """Tests verifying behaviour against data structures seen in the wild."""

    def test_real_world_example(self) -> None:
        """A complex real-world list of markdown-heavy paragraphs is returned as items."""
        raw = (
            "['Amendment to the Drinking Water Directive came into force "
            "see [press release](http://example.com).', "
            "'A proposal for a regulation on minimum requirements was adopted in May 2018.']"
        )
        result = extract(raw)
        assert result == [
            "Amendment to the Drinking Water Directive came into force see press release.",
            "A proposal for a regulation on minimum requirements was adopted in May 2018.",
        ]
