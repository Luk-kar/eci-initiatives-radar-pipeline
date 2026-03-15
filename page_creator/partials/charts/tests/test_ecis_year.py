"""Tests for data preparation logic in ecis_year.py."""

import pytest
import pandas as pd

from page_creator.partials.charts.outcomes import _LABEL_ALIASES


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Law Passed",
                "Commission Engaged",
                "Waiting for Response",  # aliased
                "Collection Ongoing",
                "Collection Ongoing",
                "Rejected Legislation",
            ],
            "registration_year": [2019, 2020, 2021, 2021, 2022, 2022],
            "title": [f"ECI {i}" for i in range(6)],
        }
    )


class TestLabelAliases:
    def test_waiting_for_response_is_aliased(self):
        df = pd.DataFrame({"current_status": ["Waiting for Response"]})
        df["current_status"] = df["current_status"].replace(_LABEL_ALIASES)
        assert df.iloc[0]["current_status"] == "Awaiting Response"

    def test_non_aliased_statuses_unchanged(self):
        statuses = ["Law Passed", "Commission Engaged", "Collection Ongoing"]
        df = pd.DataFrame({"current_status": statuses})
        df["current_status"] = df["current_status"].replace(_LABEL_ALIASES)
        assert df["current_status"].tolist() == statuses


class TestYearAggregation:
    def test_years_extracted_correctly(self, base_df):
        years = sorted(base_df["registration_year"].dropna().unique())
        assert years == [2019, 2020, 2021, 2022]

    def test_groupby_year_counts(self, base_df):
        df = base_df.copy()
        df["current_status"] = df["current_status"].replace(_LABEL_ALIASES)
        counts = df.groupby("registration_year").size()
        assert counts[2021] == 2
        assert counts[2022] == 2

    def test_missing_year_fills_zero_on_reindex(self, base_df):
        df = base_df.copy()
        df["current_status"] = df["current_status"].replace(_LABEL_ALIASES)
        law_df = df[df["current_status"] == "Law Passed"]
        years = sorted(df["registration_year"].dropna().unique())
        counts = law_df.groupby("registration_year").size().reindex(years, fill_value=0)
        assert counts[2020] == 0
        assert counts[2019] == 1
