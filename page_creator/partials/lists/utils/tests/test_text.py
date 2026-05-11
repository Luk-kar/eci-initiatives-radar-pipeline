"""Tests for truncate in utils/text.py."""

import pandas as pd
import pytest

from page_creator.partials.lists.utils.text import (
    truncate,
    wrap_initiative_title,
    strip_markdown_links,
    strip_boilerplate_headers,
)
from page_creator.partials.lists.utils.constants import DEFAULT_TRUNCATE


class TestWrapInitiativeTitle:
    def test_short_title_unchanged(self):
        title = "Short ECI title"
        result = wrap_initiative_title(title)

        assert result == title

    def test_long_single_segment_splits_on_spaces_only(self):
        # > 50 chars, with spaces before and after position 50
        title = (
            "Demand the full suspension of the EU-Israel Association "
            "Agreement in view of Israel’s violations of human rights"
        )

        result = wrap_initiative_title(title)

        # There should be exactly one <br> for this particular title
        assert "<br>" in result
        assert result.count("<br>") == 1

        br_index = result.index("<br>")

        # 1) Break must not be at the very beginning
        assert br_index > 0

        # 2) Break must come after a space (word boundary)
        assert result[br_index : br_index + 4] == "<br>"
        char_before_break = result[br_index - 1]
        assert char_before_break.isascii() and char_before_break.isalpha()

        # 3) Break must be before or at the 50‑character threshold
        assert br_index <= 50

        # 4) Left side has no trailing spaces
        left = result[:br_index]
        assert left == left.rstrip()

        # 5) Right side starts with the continuation of a word, not a space
        right = result[br_index + len("<br>") :]
        assert not right.startswith(" ")

    def test_punctuation_creates_separate_segments(self):

        title = "Part one: second part. Third part!"
        result = wrap_initiative_title(title)

        # The punctuation split happens before _split_part
        assert "Part one" in result
        assert "second part" in result
        assert "Third part" in result

    def test_orphan_merge_keeps_small_tail_with_previous_line(self):

        # Force a short final segment so _merge_orphans can act.
        title = (
            "This is a reasonably long European Citizens Initiative "
            "title with a tiny tail"
        )

        result = wrap_initiative_title(title)

        # Split into logical lines first
        lines = result.split("<br>")

        # Sanity: more than one line, so split/merge logic actually ran
        assert len(lines) == 2

        # The last line should contain both "tiny" and "tail" together,
        # not leave "tail" orphaned on its own line.
        last_line = lines[-1].strip()
        last_words = last_line.split()

        assert "tiny tail" in last_line
        assert len(last_words) >= 2

    def test_respects_total_character_budget(self):
        # Build something much longer than DEFAULT_TRUNCATE

        title = "Very long ECI title " * 20
        result = wrap_initiative_title(title)

        assert len(result) <= DEFAULT_TRUNCATE

    def test_none_raises_value_error(self):

        with pytest.raises(ValueError):
            wrap_initiative_title(None)  # type: ignore[arg-type]

    def test_non_string_raises_type_error(self):

        with pytest.raises(TypeError):
            wrap_initiative_title(123)  # type: ignore[arg-type]

    def test_empty_or_whitespace_raises_value_error(self):

        with pytest.raises(ValueError):
            wrap_initiative_title("")

        with pytest.raises(ValueError):
            wrap_initiative_title("   ")

    def test_none_raises(self):
        with pytest.raises(ValueError, match="must not be None"):
            wrap_initiative_title(None)

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="empty or whitespace"):
            wrap_initiative_title("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="empty or whitespace"):
            wrap_initiative_title("   ")

    def test_invalid_type_raises(self):
        with pytest.raises(TypeError, match="expected str"):
            wrap_initiative_title(123)


class TestStripMarkdownLinks:

    def test_basic_link(self):
        assert strip_markdown_links("See [this](http://example.com).") == "See this."

    def test_multiple_links(self):
        assert strip_markdown_links("[A](url1) and [B](url2)") == "A and B"

    def test_no_links_unchanged(self):
        assert strip_markdown_links("No links here.") == "No links here."

    def test_nan_returns_empty(self):
        assert strip_markdown_links(float("nan")) == ""

    def test_none_returns_empty(self):
        assert strip_markdown_links(None) == ""


class TestTruncate:
    def test_short_text_unchanged(self):

        assert truncate("Hello") == "Hello"

    def test_exact_max_len_unchanged(self):

        text = "A" * DEFAULT_TRUNCATE
        assert truncate(text) == text

    def test_over_max_len_truncated(self):

        text = "A" * (DEFAULT_TRUNCATE + 10)
        result = truncate(text)
        assert len(result) == DEFAULT_TRUNCATE
        assert result.endswith("…")

    def test_custom_max_len(self):

        result = truncate("Hello World", max_len=5)
        assert result == "Hell…"

    def test_none_returns_empty_string(self):

        assert truncate(None) == ""

    def test_nan_returns_empty_string(self):

        assert truncate(float("nan")) == ""

    def test_pd_na_returns_empty_string(self):

        import pandas as pd

        assert truncate(pd.NA) == ""

    def test_numeric_input_coerced_to_string(self):

        result = truncate(12345)
        assert result == "12345"

    def test_empty_string_returns_empty_string(self):

        assert truncate("") == ""

    def test_exactly_one_over_appends_ellipsis(self):

        text = "A" * (DEFAULT_TRUNCATE + 1)
        result = truncate(text)
        assert result.endswith("…")
        assert len(result) == DEFAULT_TRUNCATE


class TestStripBoilerplateHeaders:

    def test_removes_known_header(self):
        text = "Main conclusions of the Communication:\nReal content."
        assert strip_boilerplate_headers(text) == "Real content."

    def test_no_match_unchanged(self):
        assert strip_boilerplate_headers("Regular text.") == "Regular text."

    def test_invalid_type_raises(self):
        with pytest.raises(TypeError):
            strip_boilerplate_headers(123)
