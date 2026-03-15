"""Tests for data logic in signatures_cohorts.py."""

import numpy as np
import pandas as pd
import pytest

from page_creator.partials.charts.signatures_cohorts import (
    _filter_valid_signatures,
    _split_bins,
    _get_bin_ecis,
    _colorize_below,
    _colorize_above,
    ECI_THRESHOLD,
    NUM_BINS,
)


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "signatures_collected": [500_000, 1_200_000, None, 300_000, 2_000_000, 0],
            "title": ["A", "B", "C", "D", "E", "F"],
        }
    )


class TestFilterValidSignatures:
    def test_drops_null_rows(self, base_df):
        result = _filter_valid_signatures(base_df)
        assert result["signatures_collected"].notna().all()

    def test_correct_row_count(self, base_df):
        result = _filter_valid_signatures(base_df)
        assert len(result) == 5

    def test_preserves_zero(self, base_df):
        result = _filter_valid_signatures(base_df)
        assert 0 in result["signatures_collected"].values

    def test_empty_df_returns_empty(self):
        df = pd.DataFrame({"signatures_collected": [None, None], "title": ["A", "B"]})
        assert _filter_valid_signatures(df).empty


class TestSplitBins:
    def test_returns_two_arrays(self):
        below, above = _split_bins(3_000_000)
        assert isinstance(below, np.ndarray)
        assert isinstance(above, np.ndarray)

    def test_below_all_under_threshold(self):
        below, _ = _split_bins(3_000_000)
        assert all(b < ECI_THRESHOLD for b in below)

    def test_above_all_at_or_over_threshold(self):
        _, above = _split_bins(3_000_000)
        assert all(a >= ECI_THRESHOLD for a in above)

    def test_total_bin_count(self):
        below, above = _split_bins(3_000_000)
        assert len(below) + len(above) == NUM_BINS + 1


class TestGetBinEcis:
    def test_returns_titles_in_range(self, base_df):
        result = _get_bin_ecis(base_df, 200_000, 600_000)
        assert "A" in result
        assert "D" in result

    def test_excludes_out_of_range(self, base_df):
        result = _get_bin_ecis(base_df, 200_000, 600_000)
        assert "B" not in result

    def test_empty_bin_returns_no_ecis(self, base_df):
        result = _get_bin_ecis(base_df, 5_000_000, 6_000_000)
        assert result == "No ECIs"


class TestColorize:
    def test_below_returns_rgb_strings(self):
        centers = np.array([100_000, 500_000, 900_000])
        colors = _colorize_below(centers)
        assert len(colors) == 3
        assert all(c.startswith("rgb(") for c in colors)

    def test_above_returns_rgb_strings(self):
        centers = np.array([1_100_000, 1_500_000, 2_000_000])
        colors = _colorize_above(centers)
        assert len(colors) == 3
        assert all(c.startswith("rgb(") for c in colors)

    def test_below_zero_center_does_not_crash(self):
        colors = _colorize_below(np.array([0.0]))
        assert len(colors) == 1

    def test_above_clips_ratio_at_1(self):
        colors = _colorize_above(np.array([ECI_THRESHOLD * 100]))
        assert len(colors) == 1
