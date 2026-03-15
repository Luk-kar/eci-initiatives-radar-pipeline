"""Tests for normalise_registration_date in utils/dates.py."""

import datetime
import pytest
import pandas as pd

from page_creator.partials.lists.utils.dates import normalise_registration_date


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "registration_date": [
                "01/01/2015",
                "15/11/2021",
                "28/02/2019",
                "31/12/2023",
            ],
            "title": ["A", "B", "C", "D"],
        }
    )


class TestNormaliseRegistrationDate:
    def test_returns_formatted_strings(self, base_df):

        result = normalise_registration_date(base_df)
        for v in result["registration_date"]:
            assert isinstance(v, str)

    def test_correct_format(self, base_df):

        result = normalise_registration_date(base_df)
        # "1 Jan 2015", "15 Nov 2021", etc.
        assert result.iloc[0]["registration_date"] == "1 Jan 2015"
        assert result.iloc[1]["registration_date"] == "15 Nov 2021"
        assert result.iloc[2]["registration_date"] == "28 Feb 2019"
        assert result.iloc[3]["registration_date"] == "31 Dec 2023"

    def test_does_not_mutate_original(self, base_df):

        original = base_df["registration_date"].tolist()
        normalise_registration_date(base_df)
        assert base_df["registration_date"].tolist() == original

    def test_single_digit_day_has_no_leading_zero(self):

        df = pd.DataFrame({"registration_date": ["05/03/2020"]})
        result = normalise_registration_date(df)
        assert result.iloc[0]["registration_date"] == "5 Mar 2020"

    def test_invalid_date_raises(self):

        df = pd.DataFrame({"registration_date": ["not-a-date"]})
        with pytest.raises(Exception):
            normalise_registration_date(df)

    def test_empty_df_returns_empty(self):

        df = pd.DataFrame({"registration_date": pd.Series([], dtype=str)})
        result = normalise_registration_date(df)
        assert result.empty

    def test_other_columns_preserved(self, base_df):

        result = normalise_registration_date(base_df)
        assert "title" in result.columns
        assert result["title"].tolist() == base_df["title"].tolist()
