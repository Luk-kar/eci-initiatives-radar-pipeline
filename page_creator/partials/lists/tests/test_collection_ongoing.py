"""Tests for _filter and _sort logic in collection_ongoing.py."""

import pandas as pd
import pytest

from page_creator.partials.lists.collection_ongoing import _filter, _sort


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Collection Ongoing",
                "Collection Ongoing",
                "Collection Unsuccessful",
                "Law Passed",
                "Collection Ongoing",
            ],
            "title": ["A", "B", "C", "D", "E"],
            "timeline_collection_start": [
                "01/06/2024",
                "01/01/2024",
                "01/03/2023",
                "01/04/2022",
                "01/09/2024",
            ],
            "timeline_collection_closed": [None, None, None, None, "15/09/2025"],
            "signatures_collected": [500_000, 200_000, 800_000, 1_200_000, 300_000],
            "signatures_countries_threshold_met_count": [5, 3, 8, 13, 2],
            "initiative_url": ["u1", "u2", "u3", "u4", "u5"],
            "objective": ["o1", "o2", "o3", "o4", "o5"],
        }
    )


class TestFilter:
    def test_keeps_only_collection_ongoing(self, base_df):
        result = _filter(base_df)
        assert set(result["current_status"].unique()) == {"Collection Ongoing"}

    def test_excludes_other_statuses(self, base_df):
        result = _filter(base_df)
        assert "Collection Unsuccessful" not in result["current_status"].values
        assert "Law Passed" not in result["current_status"].values

    def test_correct_row_count(self, base_df):
        assert len(_filter(base_df)) == 3

    def test_returns_copy_not_original(self, base_df):
        result = _filter(base_df)
        result.loc[result.index[0], "title"] = "MODIFIED"
        assert base_df.loc[0, "title"] == "A"

    def test_empty_input_returns_empty(self):
        df = pd.DataFrame(columns=["current_status", "title"])
        assert _filter(df).empty

    def test_all_other_statuses_returns_empty(self, base_df):
        df = base_df[base_df["current_status"] != "Collection Ongoing"].copy()
        assert _filter(df).empty


class TestSort:
    def test_open_without_closed_date_come_first(self, base_df):

        filtered = _filter(base_df)
        sorted_df = _sort(filtered)
        # E has a closed date — it must appear last
        assert sorted_df.iloc[-1]["title"] == "E"

    def test_open_initiatives_ordered_by_start_date_ascending(self, base_df):

        filtered = _filter(base_df)
        sorted_df = _sort(filtered)
        open_only = sorted_df[sorted_df["timeline_collection_closed"].isna()]
        start_dates = pd.to_datetime(
            open_only["timeline_collection_start"], dayfirst=True
        )
        assert start_dates.is_monotonic_increasing

    def test_helper_columns_not_in_result(self, base_df):

        result = _sort(_filter(base_df))
        assert "_start_dt" not in result.columns
        assert "_has_closed" not in result.columns

    def test_index_is_reset(self, base_df):

        result = _sort(_filter(base_df))
        assert list(result.index) == list(range(len(result)))

    def test_all_rows_preserved_after_sort(self, base_df):

        filtered = _filter(base_df)
        sorted_df = _sort(filtered)
        assert len(sorted_df) == len(filtered)

    def test_single_row_unchanged(self):

        df = pd.DataFrame(
            {
                "current_status": ["Collection Ongoing"],
                "title": ["Only"],
                "timeline_collection_start": ["10/10/2024"],
                "timeline_collection_closed": [None],
                "signatures_collected": [100_000],
                "signatures_countries_threshold_met_count": [1],
                "initiative_url": ["u"],
                "objective": ["o"],
            }
        )
        result = _sort(df)
        assert len(result) == 1
        assert result.iloc[0]["title"] == "Only"
