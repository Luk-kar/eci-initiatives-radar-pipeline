"""Tests for data logic in top_10_signatures.py."""

import pytest
import pandas as pd

from page_creator.partials.charts.top_10_signatures import (
    _bar_color,
    _aggregate_top10,
    ECI_THRESHOLD,
)


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "title": [f"ECI {i}" for i in range(15)],
            "signatures_collected": [i * 100_000 for i in range(15)],
            "signatures_threshold_met": [i % 14 for i in range(15)],
            "objective": [f"obj {i}" for i in range(15)],
            "commission_answer_text": [f"ans {i}" for i in range(15)],
            "url": [f"https://example.com/{i}" for i in range(15)],
            "registration_year": [2012 + i for i in range(15)],
        }
    )


class TestBarColor:
    def test_below_threshold_returns_rgb(self):
        color = _bar_color(500_000, 2_000_000)
        assert color.startswith("rgb(")

    def test_above_threshold_returns_rgb(self):
        color = _bar_color(1_500_000, 2_000_000)
        assert color.startswith("rgb(")

    def test_exact_threshold_is_above(self):
        color_at = _bar_color(ECI_THRESHOLD, 2_000_000)
        color_below = _bar_color(ECI_THRESHOLD - 1, 2_000_000)
        # both return rgb — just verify they don't crash and differ
        assert color_at != color_below

    def test_zero_signatures_does_not_crash(self):
        color = _bar_color(0, 2_000_000)
        assert color.startswith("rgb(")

    def test_max_equals_threshold_does_not_crash(self):
        color = _bar_color(ECI_THRESHOLD, ECI_THRESHOLD)
        assert color.startswith("rgb(")


class TestAggregateTop10:
    def test_returns_at_most_10_rows(self, base_df):
        result = _aggregate_top10(base_df)
        assert len(result) <= 10

    def test_sorted_ascending_by_signatures(self, base_df):
        result = _aggregate_top10(base_df)
        sigs = result["signatures_collected"].tolist()
        assert sigs == sorted(sigs)

    def test_top_10_are_highest_signatures(self, base_df):
        result = _aggregate_top10(base_df)
        top_sigs = set(result["signatures_collected"].tolist())
        all_sigs = sorted(base_df["signatures_collected"].tolist(), reverse=True)[:10]
        assert top_sigs == set(all_sigs)

    def test_fewer_than_10_rows_returns_all(self):
        df = pd.DataFrame(
            {
                "title": ["A", "B", "C"],
                "signatures_collected": [100, 200, 300],
                "signatures_threshold_met": [1, 2, 3],
                "objective": ["o", "o", "o"],
                "commission_answer_text": ["a", "a", "a"],
                "url": ["u", "u", "u"],
                "registration_year": [2020, 2021, 2022],
            }
        )
        result = _aggregate_top10(df)
        assert len(result) == 3

    def test_objective_column_present(self, base_df):
        result = _aggregate_top10(base_df)
        assert "objective" in result.columns


class TestBarColorGradient:
    def test_higher_below_threshold_closer_to_yellow(self):
        low = _bar_color(100_000, 2_000_000)
        high = _bar_color(900_000, 2_000_000)
        # extract green channel — higher ratio → more green
        g_low = int(low.split(",")[1].strip())
        g_high = int(high.split(",")[1].strip())
        assert g_high > g_low
