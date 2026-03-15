"""Tests for shared hover-tooltip helpers in charts/utils.py."""

import pytest

from page_creator.partials.charts.utils import hover_item_list, hover_wrap


class TestHoverItemList:
    def test_empty_list_returns_none(self):
        assert hover_item_list([]) == "None"

    def test_single_item(self):
        result = hover_item_list(["ECI Alpha"])
        assert result == "• ECI Alpha"

    def test_multiple_items_joined_with_br(self):
        result = hover_item_list(["A", "B", "C"])
        assert result == "• A<br>• B<br>• C"

    def test_truncates_at_max_items(self):
        titles = [f"ECI {i}" for i in range(15)]
        result = hover_item_list(titles, max_items=10)
        assert "and 5 more" in result

    def test_exactly_max_items_no_suffix(self):
        titles = [f"ECI {i}" for i in range(10)]
        result = hover_item_list(titles, max_items=10)
        assert "more" not in result

    def test_custom_max_items(self):
        result = hover_item_list(["A", "B", "C", "D"], max_items=2)
        assert "and 2 more" in result


class TestHoverWrap:
    def test_short_text_unchanged(self):
        result = hover_wrap("Hello world")
        assert result == "Hello world"

    def test_long_text_broken_into_br_lines(self):
        text = "word " * 30
        result = hover_wrap(text)
        assert "<br>" in result

    def test_truncated_to_max_lines(self):
        text = "word " * 100
        result = hover_wrap(text, max_lines=3)
        lines = result.split("<br>")
        assert len(lines) <= 3

    def test_truncated_line_ends_with_ellipsis(self):
        text = "word " * 100
        result = hover_wrap(text, max_lines=3)
        assert result.endswith("…")

    def test_exactly_max_lines_no_ellipsis(self):
        # 3 words of 4 chars each fit in one line at width=60 → 1 line, no ellipsis
        result = hover_wrap("word word word", width=60, max_lines=3)
        assert not result.endswith("…")

    def test_non_string_input_coerced(self):
        result = hover_wrap(12345)
        assert result == "12345"
