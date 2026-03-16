"""Tests for sig_cell and threshold_cell in utils/signatures.py."""

from page_creator.partials.lists.utils.signatures import sig_cell, threshold_cell
from page_creator.partials.lists.utils.constants import SIG_TARGET, COUNTRIES_THRESHOLD


class TestSigCell:
    def test_none_returns_collection_not_started(self):

        assert sig_cell(None) == "Collection not started"

    def test_nan_returns_collection_not_started(self):

        assert sig_cell(float("nan")) == "Collection not started"

    def test_zero_returns_formatted_zero(self):

        result = sig_cell(0)
        assert result.startswith("0")
        assert "Collection not started" not in result

    def test_value_formatted_with_commas(self):

        result = sig_cell(1_234_567)
        assert "1,234,567" in result

    def test_contains_progress_bar(self):

        assert "progress-bar" in sig_cell(500_000)

    def test_exact_target_shows_100_percent_bar(self):

        result = sig_cell(SIG_TARGET)
        assert "width:100.0%" in result

    def test_above_target_shows_over_class(self):

        result = sig_cell(SIG_TARGET + 1)
        assert "progress-bar__fill--over" in result

    def test_half_target_shows_50_percent(self):

        result = sig_cell(SIG_TARGET // 2)
        assert "width:50.0%" in result

    def test_uses_signatures_modifier(self):

        assert "progress-bar__fill--signatures" in sig_cell(500_000)


class TestThresholdCell:
    def test_none_returns_collection_not_started(self):

        assert threshold_cell(None) == "Collection not started"

    def test_nan_returns_collection_not_started(self):

        assert threshold_cell(float("nan")) == "Collection not started"

    def test_zero_shows_zero_of_threshold(self):

        result = threshold_cell(0)
        assert f"0 / {COUNTRIES_THRESHOLD}" in result
        assert "Collection not started" not in result

    def test_value_shows_n_of_threshold(self):

        result = threshold_cell(5)
        assert f"5 / {COUNTRIES_THRESHOLD}" in result

    def test_contains_progress_bar(self):

        assert "progress-bar" in threshold_cell(3)

    def test_exact_threshold_shows_100_percent(self):

        result = threshold_cell(COUNTRIES_THRESHOLD)
        assert "width:100.0%" in result

    def test_above_threshold_shows_over_class(self):

        result = threshold_cell(COUNTRIES_THRESHOLD + 1)
        assert "progress-bar__fill--over" in result

    def test_uses_threshold_modifier(self):

        assert "progress-bar__fill--threshold" in threshold_cell(3)
