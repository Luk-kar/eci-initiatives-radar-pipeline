"""Tests for _sort logic in total_initiatives.py."""

import datetime

import pandas as pd
import pytest

from page_creator.partials.lists.total_initiatives import _sort


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Collection Ongoing",
                "Law Passed",
                "Rejected Legislation",
                "Collection Unsuccessful",
                "Withdrawn",
            ],
            "title": ["A", "B", "C", "D", "E"],
            "registration_date": [
                "15/03/2023",
                "01/01/2015",
                "20/07/2019",
                "10/10/2012",
                "05/05/2017",
            ],
            "signatures_collected": [300_000, 1_200_000, 1_100_000, 500_000, None],
            "signatures_threshold_met": [3, 13, 10, 4, None],
            "url": [f"u{i}" for i in range(5)],
            "objective": [f"o{i}" for i in range(5)],
        }
    )


class TestSort:
    def test_no_rows_filtered_out(self, base_df):

        result = _sort(base_df)
        assert len(result) == len(base_df)

    def test_all_statuses_present(self, base_df):

        result = _sort(base_df)
        assert set(result["current_status"]) == set(base_df["current_status"])

    def test_sorted_by_registration_date_descending(self, base_df):

        result = _sort(base_df)
        dates = result["registration_date"].tolist()
        assert dates == sorted(dates, reverse=True)

    def test_registration_date_is_date_type(self, base_df):

        result = _sort(base_df)
        assert all(isinstance(d, datetime.date) for d in result["registration_date"])

    def test_most_recent_first(self, base_df):

        # "A" registered 15/03/2023 is the most recent
        result = _sort(base_df)
        assert result.iloc[0]["title"] == "A"

    def test_oldest_last(self, base_df):

        # "D" registered 10/10/2012 is the oldest
        result = _sort(base_df)
        assert result.iloc[-1]["title"] == "D"

    def test_index_is_reset(self, base_df):

        result = _sort(base_df)
        assert list(result.index) == list(range(len(result)))

    def test_does_not_mutate_original(self, base_df):

        original_dates = base_df["registration_date"].tolist()
        _sort(base_df)
        assert base_df["registration_date"].tolist() == original_dates

    def test_null_signatures_rows_preserved(self, base_df):

        result = _sort(base_df)
        assert result["signatures_collected"].isna().sum() == 1

    def test_single_row_unchanged(self):
        df = pd.DataFrame(
            {
                "title": ["Solo"],
                "registration_date": ["01/06/2021"],
                "current_status": ["Withdrawn"],
                "signatures_collected": [50_000],
                "signatures_threshold_met": [1],
                "url": ["u"],
                "objective": ["o"],
            }
        )
        result = _sort(df)
        assert len(result) == 1
        assert isinstance(result.iloc[0]["registration_date"], datetime.date)

    def test_null_signatures_renders_collection_not_started(self):
        df = pd.DataFrame(
            {
                "title": ["No Sigs"],
                "registration_date": ["01/06/2021"],
                "current_status": ["Collection Ongoing"],
                "signatures_collected": [None],
                "signatures_threshold_met": [None],
                "url": ["u"],
                "objective": ["o"],
            }
        )
        result = _sort(df)
        assert pd.isna(result.iloc[0]["signatures_collected"])
        assert pd.isna(result.iloc[0]["signatures_threshold_met"])

    def test_zero_signatures_does_not_render_collection_not_started(self):
        df = pd.DataFrame(
            {
                "title": ["Zero Sigs"],
                "registration_date": ["01/06/2021"],
                "current_status": ["Collection Ongoing"],
                "signatures_collected": [0],
                "signatures_threshold_met": [0],
                "url": ["u"],
                "objective": ["o"],
            }
        )
        result = _sort(df)
        assert result.iloc[0]["signatures_collected"] == 0
        assert result.iloc[0]["signatures_threshold_met"] == 0
