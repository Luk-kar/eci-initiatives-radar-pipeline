"""Tests for _filter and _sort logic in reached_signatures.py."""

import datetime

import pandas as pd
import pytest

from page_creator.partials.lists.reached_signatures import _filter, _sort
from page_creator.partials.lists.utils import SIG_TARGET


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Commission Engaged",
                "Rejected Legislation",
                "Commission Engaged",
                "Collection Unsuccessful",
                "Law Passed",
            ],
            "title": ["A", "B", "C", "D", "E"],
            "registration_date": [
                "01/01/2013",
                "01/01/2015",
                "01/01/2019",
                "01/01/2020",
                "01/01/2017",
            ],
            "signatures_collected": [
                1_884_790,  # above threshold
                1_173_130,  # above threshold
                800_000,  # below threshold
                236_000,  # below threshold
                1_050_000,  # above threshold
            ],
            "signatures_countries_threshold_met_count": [13, 11, 3, 2, 7],
            "initiative_url": [f"u{i}" for i in range(5)],
            "objective": [f"o{i}" for i in range(5)],
        }
    )


class TestFilter:
    def test_keeps_only_rows_above_sig_target(self, base_df):

        result = _filter(base_df)
        assert all(result["signatures_collected"] >= SIG_TARGET)

    def test_excludes_rows_below_sig_target(self, base_df):

        result = _filter(base_df)
        assert "C" not in result["title"].values
        assert "D" not in result["title"].values

    def test_correct_row_count(self, base_df):

        assert len(_filter(base_df)) == 3

    def test_empty_input_returns_empty(self):

        df = pd.DataFrame(columns=["signatures_collected"])
        assert _filter(df).empty

    def test_all_below_threshold_returns_empty(self, base_df):

        df = base_df[base_df["signatures_collected"] < SIG_TARGET].copy()
        assert _filter(df).empty

    def test_exact_sig_target_is_included(self):

        df = pd.DataFrame(
            {
                "signatures_collected": [SIG_TARGET],
                "title": ["Exact"],
                "registration_date": ["01/01/2020"],
            }
        )
        assert len(_filter(df)) == 1

    def test_one_below_sig_target_is_excluded(self):

        df = pd.DataFrame(
            {
                "signatures_collected": [SIG_TARGET - 1],
                "title": ["AlmostThere"],
                "registration_date": ["01/01/2020"],
            }
        )
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

        # E has 01/01/2017, A has 01/01/2013, B has 01/01/2015 → E is most recent
        result = _sort(_filter(base_df))
        assert result.iloc[0]["title"] == "E"

    def test_row_count_unchanged_after_sort(self, base_df):

        filtered = _filter(base_df)
        assert len(_sort(filtered)) == len(filtered)
