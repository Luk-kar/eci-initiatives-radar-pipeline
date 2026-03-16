"""Tests for data logic in bubble_finance_plot.py."""

import numpy as np
import pandas as pd
import pytest

from page_creator.partials.charts.bubble_finance_plot import (
    _format_amount,
    _parse_funding,
    _prepare_dataframe,
    _add_jitter,
    _compute_marker_sizes,
    _build_hover,
    _present_categories,
    _COMMISSION_ANSWER_FALLBACK,
    _STATUS_ALIASES,
    BUBBLE_COLORS,
    _LOG_ZERO_DISPLAY,
)


# ── Fixtures ───────────────────────────────────────────────────────────────


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "title": ["ECI A", "ECI B", "ECI C"],
            "current_status": [
                "Law Passed",
                "Collection Ongoing",
                "Rejected Legislation",
            ],
            "funding_total": ["1,000.00", "500", "0"],
            "objective": ["obj a", "obj b", "obj c"],
            "commission_answer_text": ["ans a", None, "ans c"],
            "url": ["https://a.com", "https://b.com", "https://c.com"],
        }
    )


@pytest.fixture
def prepared_df(base_df):
    return _prepare_dataframe(base_df)


# ── TestFormatAmount ───────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value, expected",
    [
        # Below 1K — no suffix
        (0, "€0"),
        (1, "€1"),
        (847, "€847"),
        (999, "€999"),
        # Exact thresholds — no decimal
        (1_000, "€1K"),
        (10_000, "€10K"),
        (100_000, "€100K"),
        (1_000_000, "€1M"),
        (10_000_000, "€10M"),
        (1_000_000_000, "€1B"),
        # With decimal
        (1_500, "€1.5K"),
        (94_300, "€94.3K"),
        (4_823_150, "€4.8M"),
        (2_100_000_000, "€2.1B"),
        # Rounds correctly
        (1_100_000, "€1.1M"),
        (1_050_000, "€1.1M"),
    ],
)
def test_format_amount(value: float, expected: str) -> None:
    assert _format_amount(value) == expected


# ── TestParseFunding ───────────────────────────────────────────────────────


class TestParseFunding:
    def test_comma_formatted_string(self):
        assert _parse_funding("12,980.15") == pytest.approx(12980.15)

    def test_plain_string(self):
        assert _parse_funding("500") == pytest.approx(500.0)

    def test_integer(self):
        assert _parse_funding(1000) == pytest.approx(1000.0)

    def test_float(self):
        assert _parse_funding(3.14) == pytest.approx(3.14)

    def test_zero_string(self):
        assert _parse_funding("0") == pytest.approx(0.0)

    def test_nan_returns_zero(self):
        assert _parse_funding(float("nan")) == 0.0

    def test_none_returns_zero(self):
        assert _parse_funding(None) == 0.0

    def test_empty_string_returns_zero(self):
        assert _parse_funding("") == 0.0

    def test_invalid_string_returns_zero(self):
        assert _parse_funding("not-a-number") == 0.0


# ── TestPrepareDataframe ───────────────────────────────────────────────────


class TestPrepareDataframe:
    def test_known_statuses_kept(self, base_df):
        result = _prepare_dataframe(base_df)
        assert set(result["bubble_category"]).issubset(BUBBLE_COLORS.keys())

    def test_unknown_statuses_dropped(self):
        df = pd.DataFrame(
            {
                "title": ["X"],
                "current_status": ["Unknown Status"],
                "funding_total": ["100"],
                "objective": ["o"],
                "commission_answer_text": ["a"],
                "url": ["https://x.com"],
            }
        )
        result = _prepare_dataframe(df)
        assert len(result) == 0

    def test_status_aliases_resolved(self):
        for alias, target in _STATUS_ALIASES.items():
            df = pd.DataFrame(
                {
                    "title": ["Y"],
                    "current_status": [alias],
                    "funding_total": ["100"],
                    "objective": ["o"],
                    "commission_answer_text": ["a"],
                    "url": ["https://y.com"],
                }
            )
            result = _prepare_dataframe(df)
            assert result["bubble_category"].iloc[0] == target

    def test_zero_funding_sets_log_zero_display(self):
        df = pd.DataFrame(
            {
                "title": ["Z"],
                "current_status": ["Law Passed"],
                "funding_total": [0],
                "objective": ["o"],
                "commission_answer_text": ["a"],
                "url": ["https://z.com"],
            }
        )
        result = _prepare_dataframe(df)
        assert result["funding_display"].iloc[0] == _LOG_ZERO_DISPLAY

    def test_nonzero_funding_preserved(self):
        df = pd.DataFrame(
            {
                "title": ["Z"],
                "current_status": ["Law Passed"],
                "funding_total": ["5000"],
                "objective": ["o"],
                "commission_answer_text": ["a"],
                "url": ["https://z.com"],
            }
        )
        result = _prepare_dataframe(df)
        assert result["funding_display"].iloc[0] == pytest.approx(5000.0)

    def test_has_zero_funding_flag(self):
        df = pd.DataFrame(
            {
                "title": ["A", "B"],
                "current_status": ["Law Passed", "Law Passed"],
                "funding_total": [0, "1000"],
                "objective": ["o", "o"],
                "commission_answer_text": ["a", "a"],
                "url": ["https://a.com", "https://b.com"],
            }
        )
        result = _prepare_dataframe(df)
        assert result.loc[result["title"] == "A", "has_zero_funding"].iloc[0] == True
        assert result.loc[result["title"] == "B", "has_zero_funding"].iloc[0] == False


# ── TestAddJitter ──────────────────────────────────────────────────────────


class TestAddJitter:
    def test_y_jitter_within_range(self, prepared_df):
        present = list(prepared_df["bubble_category"].unique())
        result = _add_jitter(prepared_df, present)
        for _, row in result.iterrows():
            base = row["y_pos"]
            assert base - 0.15 <= row["y_jitter"] <= base + 0.15

    def test_y_pos_matches_category_index(self, prepared_df):
        present = list(prepared_df["bubble_category"].unique())
        result = _add_jitter(prepared_df, present)
        cat_index = {c: i for i, c in enumerate(present)}
        for _, row in result.iterrows():
            assert row["y_pos"] == cat_index[row["bubble_category"]]

    def test_jitter_is_reproducible(self, prepared_df):
        present = list(prepared_df["bubble_category"].unique())
        result1 = _add_jitter(prepared_df.copy(), present)
        result2 = _add_jitter(prepared_df.copy(), present)
        assert result1["y_jitter"].tolist() == result2["y_jitter"].tolist()


# ── TestComputeMarkerSizes ─────────────────────────────────────────────────


class TestComputeMarkerSizes:

    def test_no_nan_in_sizes(self, prepared_df):
        present = list(prepared_df["bubble_category"].unique())
        df = _add_jitter(prepared_df, present)
        result = _compute_marker_sizes(df)
        assert result["marker_size"].notna().all()

    def test_single_row_does_not_crash(self):
        df = pd.DataFrame(
            {
                "title": ["Solo"],
                "current_status": ["Law Passed"],
                "funding_total": ["1000"],
                "objective": ["o"],
                "commission_answer_text": ["a"],
                "url": ["https://solo.com"],
            }
        )
        df = _prepare_dataframe(df)
        present = list(df["bubble_category"].unique())
        df = _add_jitter(df, present)
        result = _compute_marker_sizes(df)
        assert result["marker_size"].iloc[0] == 20  # span == 0 fallback


# ── TestBuildHover ─────────────────────────────────────────────────────────


class TestBuildHover:
    def test_contains_title(self):
        row = pd.Series(
            {
                "title": "My Initiative",
                "has_zero_funding": False,
                "funding_numeric": 5000.0,
                "current_status": "Law Passed",
            }
        )
        result = _build_hover(row)
        assert "My Initiative" in result

    def test_zero_funding_shows_no_data_label(self):
        row = pd.Series(
            {
                "title": "X",
                "has_zero_funding": True,
                "funding_numeric": 0.0,
                "current_status": "Law Passed",
            }
        )
        result = _build_hover(row)
        assert "No funding data" in result

    def test_nonzero_funding_formatted(self):
        row = pd.Series(
            {
                "title": "X",
                "has_zero_funding": False,
                "funding_numeric": 12500.0,
                "current_status": "Law Passed",
            }
        )
        result = _build_hover(row)
        assert "12,500" in result

    def test_title_truncated_at_65_chars(self):
        row = pd.Series(
            {
                "title": "A" * 100,
                "has_zero_funding": False,
                "funding_numeric": 1000.0,
                "current_status": "Law Passed",
            }
        )
        result = _build_hover(row)
        assert "A" * 66 not in result


# ── TestPresentCategories ──────────────────────────────────────────────────


class TestPresentCategories:
    def test_returns_only_present(self, prepared_df):
        present = _present_categories(prepared_df)
        all_categories = list(BUBBLE_COLORS.keys())
        absent = [
            c for c in all_categories if c not in prepared_df["bubble_category"].values
        ]
        for cat in absent:
            assert cat not in present


# ── TestCommissionAnswerFallback ───────────────────────────────────────────


class TestCommissionAnswerFallback:
    @pytest.mark.parametrize("status", _COMMISSION_ANSWER_FALLBACK.keys())
    def test_fallback_keys_are_valid_bubble_categories_or_aliases(self, status):
        all_valid = set(BUBBLE_COLORS.keys()) | set(_STATUS_ALIASES.keys())
        assert status in all_valid

    @pytest.mark.parametrize("status", _COMMISSION_ANSWER_FALLBACK.keys())
    def test_fallback_values_are_non_empty_strings(self, status):
        value = _COMMISSION_ANSWER_FALLBACK[status]
        assert isinstance(value, str) and len(value) > 0
