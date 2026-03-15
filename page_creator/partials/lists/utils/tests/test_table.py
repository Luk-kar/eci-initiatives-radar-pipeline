"""Tests for build_table and wrap_table_card in utils/table.py."""

import pandas as pd
import pytest
from page_creator.partials.lists.utils.table import build_table, wrap_table_card
from page_creator.partials.lists.utils.constants import SCROLL_THRESHOLD


HEADERS = ["Col A", "Col B", "Col C"]
ROWS_HTML = "<tr><td>1</td><td>2</td><td>3</td></tr>"


class TestBuildTable:
    def test_contains_table_class(self):

        assert 'class="data-table"' in build_table(HEADERS, ROWS_HTML)

    def test_headers_rendered_as_th(self):

        result = build_table(HEADERS, ROWS_HTML)
        for h in HEADERS:
            assert f"<th>{h}</th>" in result

    def test_rows_included_in_tbody(self):

        result = build_table(HEADERS, ROWS_HTML)
        assert ROWS_HTML in result

    def test_not_scrollable_by_default(self):

        result = build_table(HEADERS, ROWS_HTML)
        assert "data-table__scroll-wrapper" not in result

    def test_scrollable_adds_wrapper(self):

        result = build_table(HEADERS, ROWS_HTML, scrollable=True)
        assert "data-table__scroll-wrapper" in result

    def test_scrollbar_color_applied_when_scrollable(self):

        result = build_table(
            HEADERS, ROWS_HTML, scrollable=True, scrollbar_color="#abc123"
        )
        assert "--scrollbar-color:#abc123" in result

    def test_no_color_style_when_not_scrollable(self):

        result = build_table(
            HEADERS, ROWS_HTML, scrollable=False, scrollbar_color="#abc123"
        )
        assert "--scrollbar-color" not in result

    def test_no_color_style_when_no_color_provided(self):

        result = build_table(HEADERS, ROWS_HTML, scrollable=True)
        assert "--scrollbar-color" not in result

    def test_empty_rows_still_renders_table(self):

        result = build_table(HEADERS, "")
        assert "<table" in result
        assert "<thead>" in result


class TestWrapTableCard:
    def _make_df(self, n: int) -> pd.DataFrame:

        return pd.DataFrame({"title": [f"ECI {i}" for i in range(n)]})

    def test_contains_title(self):

        result = wrap_table_card(
            "<h3>Title</h3>", ROWS_HTML, self._make_df(3), HEADERS, "#fff"
        )
        assert "<h3>Title</h3>" in result

    def test_wrapped_in_card(self):

        result = wrap_table_card(
            "<h3>T</h3>", ROWS_HTML, self._make_df(3), HEADERS, "#fff"
        )
        assert "card" in result

    def test_not_scrollable_below_threshold(self):

        df = self._make_df(SCROLL_THRESHOLD)
        result = wrap_table_card("<h3>T</h3>", ROWS_HTML, df, HEADERS, "#fff")
        assert "data-table__scroll-wrapper" not in result

    def test_scrollable_above_threshold(self):

        df = self._make_df(SCROLL_THRESHOLD + 1)
        result = wrap_table_card("<h3>T</h3>", ROWS_HTML, df, HEADERS, "#fff")
        assert "data-table__scroll-wrapper" in result

    def test_scrollbar_color_passed_through(self):

        df = self._make_df(SCROLL_THRESHOLD + 1)
        result = wrap_table_card("<h3>T</h3>", ROWS_HTML, df, HEADERS, "#3CA371")
        assert "--scrollbar-color:#3CA371" in result
