"""Tests for truncate in utils/text.py."""

from page_creator.partials.lists.utils.text import truncate
from page_creator.partials.lists.utils.constants import DEFAULT_TRUNCATE


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
