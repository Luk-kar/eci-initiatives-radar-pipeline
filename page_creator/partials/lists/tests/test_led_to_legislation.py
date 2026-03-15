"""Tests for _filter and _sort logic in led_to_legislation.py."""

import datetime

import pandas as pd
import pytest

from page_creator.partials.lists.led_to_legislation import _filter, _sort


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Law Passed",
                "Law Passed",
                "Commission Engaged",
                "Rejected Legislation",
                "Collection Unsuccessful",
            ],
            "title": ["A", "B", "C", "D", "E"],
            "registration_date": [
                "10/04/2018",
                "01/01/2015",
                "05/06/2019",
                "20/03/2017",
                "11/11/2020",
            ],
            "url": [f"u{i}" for i in range(5)],
            "objective": [f"o{i}" for i in range(5)],
            "legislation": [
                "Directive (EU) 2020/1234 adopted.",
                "Regulation (EU) 2016/5678 adopted.",
                None,
                None,
                None,
            ],
        }
    )


class TestFilter:
    def test_keeps_only_law_passed(self, base_df):

        result = _filter(base_df)
        assert set(result["current_status"].unique()) == {"Law Passed"}

    def test_excludes_other_statuses(self, base_df):

        result = _filter(base_df)
        for excluded in (
            "Commission Engaged",
            "Rejected Legislation",
            "Collection Unsuccessful",
        ):
            assert excluded not in result["current_status"].values

    def test_correct_row_count(self, base_df):

        assert len(_filter(base_df)) == 2

    def test_empty_input_returns_empty(self):

        df = pd.DataFrame(columns=["current_status"])
        assert _filter(df).empty

    def test_no_law_passed_rows_returns_empty(self, base_df):

        df = base_df[base_df["current_status"] != "Law Passed"].copy()
        assert _filter(df).empty


class TestSort:
    def test_sorted_by_registration_date_descending(self, base_df):

        result = _sort(_filter(base_df))
        dates = result["registration_date"].tolist()
        assert dates == sorted(dates, reverse=True)

    def test_registration_date_is_date_type(self, base_df):

        result = _sort(_filter(base_df))
        assert all(isinstance(d, datetime.date) for d in result["registration_date"])

    def test_index_is_reset(self, base_df):

        result = _sort(_filter(base_df))
        assert list(result.index) == list(range(len(result)))

    def test_most_recent_first(self, base_df):

        # "A" registered 10/04/2018 > "B" registered 01/01/2015
        result = _sort(_filter(base_df))
        assert result.iloc[0]["title"] == "A"

    def test_legislation_column_preserved(self, base_df):

        result = _sort(_filter(base_df))
        assert "legislation" in result.columns
        assert result.iloc[0]["legislation"] is not None
