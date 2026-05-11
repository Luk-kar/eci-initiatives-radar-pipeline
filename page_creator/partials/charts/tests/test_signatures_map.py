"""Tests for data logic in signatures_map.py."""

import json
import pytest
import pandas as pd

from page_creator.partials.charts.signatures_map import (
    _format_sigs,
    _parse_count,
    _build_country_df,
    _COUNTRIES,
    _NAME_TO_ALPHA2,
)


@pytest.fixture
def base_df():
    country_data = {
        "Germany": {
            "signatures": "380,455",
            "threshold": 74250,
            "percentage": 512.40,
        },
        "France": {
            "signatures": "281,397",
            "threshold": 55500,
            "percentage": 507.02,
        },
        "Poland": {
            "signatures": "177,747",
            "threshold": 38250,
            "percentage": 464.70,
        },
    }
    return pd.DataFrame(
        {
            "title": ["Test ECI"],
            "signatures_collected_by_country": [json.dumps(country_data)],
        }
    )


class TestFormatSigs:
    def test_below_1k(self):
        assert _format_sigs(500) == "500"

    def test_exact_1k(self):
        assert _format_sigs(1_000) == "1K"

    def test_thousands(self):
        assert _format_sigs(94_300) == "94K"

    def test_exact_1m(self):
        assert _format_sigs(1_000_000) == "1.0M"

    def test_millions(self):
        assert _format_sigs(1_884_790) == "1.9M"

    def test_zero(self):
        assert _format_sigs(0) == "0"


class TestParseCount:
    def test_int_passthrough(self):

        assert _parse_count({"signatures": 12345}) == 12345

    def test_dict_with_comma_formatted_string(self):

        assert _parse_count({"signatures": "380,455"}) == 380455

    def test_dict_with_asterisk(self):

        assert _parse_count({"signatures": "333*"}) == 333

    def test_plain_string(self):

        assert _parse_count({"signatures": "12,980"}) == 12980

    def test_string_with_asterisk(self):

        assert _parse_count({"signatures": "333*"}) == 333


class TestBuildCountryDf:
    def test_returns_dataframe(self, base_df):
        result = _build_country_df(base_df)
        assert isinstance(result, pd.DataFrame)

    def test_has_expected_columns(self, base_df):
        result = _build_country_df(base_df)
        for col in ["alpha2", "alpha3", "name", "total", "label", "eci_list"]:
            assert col in result.columns

    def test_correct_country_count(self, base_df):
        result = _build_country_df(base_df)
        assert len(result) == 3

    def test_sorted_by_total_descending(self, base_df):
        result = _build_country_df(base_df)
        totals = result["total"].tolist()
        assert totals == sorted(totals, reverse=True)

    def test_germany_has_highest_total(self, base_df):
        result = _build_country_df(base_df)
        assert result.iloc[0]["name"] == "Germany"

    def test_threshold_met_counted_at_100pct(self, base_df):
        result = _build_country_df(base_df)
        # all three countries have percentage >= 100%
        assert (result["threshold_met_count"] >= 1).all()

    def test_empty_df_returns_empty(self):
        df = pd.DataFrame({"title": [], "signatures_collected_by_country": []})
        result = _build_country_df(df)
        assert result.empty

    def test_null_country_data_skipped(self):
        df = pd.DataFrame(
            {
                "title": ["ECI A", "ECI B"],
                "signatures_collected_by_country": [None, ""],
            }
        )
        result = _build_country_df(df)
        assert result.empty


class TestCountryLookup:
    def test_name_to_alpha2_reverse_of_countries(self):
        for alpha2, (name, *_) in _COUNTRIES.items():
            assert _NAME_TO_ALPHA2[name] == alpha2

    def test_all_27_eu_member_states_present(self):
        assert len(_COUNTRIES) == 27
