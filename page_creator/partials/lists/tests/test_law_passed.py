from unittest.mock import patch

import pandas as pd
import pytest

from page_creator.partials.lists.law_passed import _build_row, _parse_last_legislation


class TestParsLastLegislation:
    def test_empty_string_returns_empty(self):
        assert _parse_last_legislation("") == ""

    def test_none_returns_empty(self):
        assert _parse_last_legislation(None) == ""

    def test_nan_returns_empty(self):
        assert _parse_last_legislation(float("nan")) == ""
        with pytest.raises(TypeError):
            _parse_last_legislation(pd.NA)

    def test_invalid_syntax_returns_empty(self):
        assert _parse_last_legislation("[unclosed") == ""
        assert _parse_last_legislation("not a list") == ""

    def test_empty_list_returns_empty(self):
        assert _parse_last_legislation("[]") == ""

    def test_returns_last_item(self):
        assert _parse_last_legislation("['Leg 1', 'Leg 2']") == "Leg 2"


class TestBuildRowTextProcessing:

    @patch("page_creator.partials.lists.law_passed.strip_markdown_links")
    @patch("page_creator.partials.lists.law_passed.strip_boilerplate_headers")
    def test_wrap_initiative_title_called_on_title(
        self, mock_boilerplate, mock_strip_links
    ):
        mock_strip_links.side_effect = lambda x: x
        mock_boilerplate.side_effect = lambda x: x
        row = pd.Series(
            {
                "title": "Raw Title",
                "initiative_url": "http://x.com",
                "registration_date": "01/01/2020",
                "objective": "obj",
                "law_passed": "['Legislation A']",
            }
        )
        _build_row(row)

    @patch("page_creator.partials.lists.law_passed.strip_markdown_links")
    @patch("page_creator.partials.lists.law_passed.strip_boilerplate_headers")
    def test_strip_markdown_links_called_on_objective(
        self, mock_boilerplate, mock_strip_links
    ):
        mock_strip_links.side_effect = lambda x: x
        mock_boilerplate.side_effect = lambda x: x
        row = pd.Series(
            {
                "title": "T",
                "initiative_url": "http://x.com",
                "registration_date": "01/01/2020",
                "objective": "Raw Objective",
                "law_passed": "['Leg A']",
            }
        )
        _build_row(row)
        mock_strip_links.assert_any_call("Raw Objective")

    @patch("page_creator.partials.lists.law_passed.strip_markdown_links")
    @patch("page_creator.partials.lists.law_passed.strip_boilerplate_headers")
    def test_strip_markdown_links_called_on_legislation(
        self, mock_boilerplate, mock_strip_links
    ):
        mock_strip_links.side_effect = lambda x: x
        mock_boilerplate.side_effect = lambda x: x
        row = pd.Series(
            {
                "title": "T",
                "initiative_url": "http://x.com",
                "registration_date": "01/01/2020",
                "objective": "obj",
                "law_passed": "['Legislation A']",
            }
        )
        _build_row(row)
        mock_strip_links.assert_any_call(
            "Legislation A"
        )  # after _parse_last_legislation

    @patch("page_creator.partials.lists.law_passed.strip_markdown_links")
    @patch("page_creator.partials.lists.law_passed.strip_boilerplate_headers")
    def test_strip_boilerplate_headers_called_on_legislation(
        self, mock_boilerplate, mock_strip_links
    ):
        mock_strip_links.side_effect = lambda x: x
        mock_boilerplate.side_effect = lambda x: x
        row = pd.Series(
            {
                "title": "T",
                "initiative_url": "http://x.com",
                "registration_date": "01/01/2020",
                "objective": "obj",
                "law_passed": "['Legislation A']",
            }
        )
        _build_row(row)
        mock_boilerplate.assert_any_call("Legislation A")
