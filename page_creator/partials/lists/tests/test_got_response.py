"""Tests for _filter and _sort logic in got_response.py."""

import datetime

import pandas as pd
import pytest

from page_creator.partials.lists.got_response import _filter, _sort, _RESPONSE_STATUSES


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Commission Engaged",
                "Rejected Legislation",
                "Law Passed",
                "Collection Unsuccessful",
                "Collection Ongoing",
                "Withdrawn",
                "Commission Engaged",
            ],
            "title": ["A", "B", "C", "D", "E", "F", "G"],
            "registration_date": [
                "01/03/2019",
                "01/06/2017",
                "15/11/2021",
                "01/01/2015",
                "10/05/2023",
                "20/08/2016",
                "05/02/2020",
            ],
            "url": [f"u{i}" for i in range(7)],
            "objective": [f"o{i}" for i in range(7)],
            "commission_answer_text": [f"ans{i}" for i in range(7)],
        }
    )


class TestFilter:
    def test_keeps_only_response_statuses(self, base_df):

        result = _filter(base_df)
        assert set(result["current_status"].unique()).issubset(_RESPONSE_STATUSES)

    def test_excludes_non_response_statuses(self, base_df):
        result = _filter(base_df)
        for excluded in ("Collection Unsuccessful", "Collection Ongoing", "Withdrawn"):
            assert excluded not in result["current_status"].values

    def test_correct_row_count(self, base_df):

        assert (
            len(_filter(base_df)) == 4
        )  # types: "Commission Engaged", "Rejected Legislation", "Law Passed"

    def test_empty_input_returns_empty(self):

        df = pd.DataFrame(columns=["current_status"])
        assert _filter(df).empty

    def test_all_excluded_statuses_returns_empty(self, base_df):

        df = base_df[~base_df["current_status"].isin(_RESPONSE_STATUSES)].copy()
        assert _filter(df).empty

    def test_response_statuses_constant_contents(self):

        assert _RESPONSE_STATUSES == frozenset(
            {"Commission Engaged", "Law Passed", "Rejected Legislation"}
        )


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

    def test_row_count_unchanged_after_sort(self, base_df):

        filtered = _filter(base_df)
        assert len(_sort(filtered)) == len(filtered)

    def test_most_recent_first(self, base_df):

        result = _sort(_filter(base_df))
        # "C" (Law Passed) has 15/11/2021 — the most recent among the three
        assert result.iloc[0]["title"] == "C"
