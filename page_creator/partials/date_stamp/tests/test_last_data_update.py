"""Tests for generate_last_data_update in last_data_update.py."""

import pytest

from page_creator.partials.date_stamp.last_data_update import generate_last_data_update


class TestGenerateLastDataUpdate:

    def test_returns_string(self):
        result = generate_last_data_update("2026-02-09")
        assert isinstance(result, str)

    def test_contains_footer_tag(self):
        result = generate_last_data_update("2026-02-09")
        assert "<footer" in result
        assert "</footer>" in result

    def test_contains_slot_id(self):
        result = generate_last_data_update("2026-02-09")
        assert 'id="last-data-update-slot"' in result

    def test_contains_css_class(self):
        result = generate_last_data_update("2026-02-09")
        assert 'class="data-timestamp"' in result

    def test_contains_label_text(self):
        result = generate_last_data_update("2026-02-09")
        assert "Last data retrieved:" in result

    def test_formats_date_correctly(self):
        result = generate_last_data_update("2026-02-09")
        assert "9 Feb 2026" in result

    def test_formats_date_no_leading_zero_on_day(self):
        result = generate_last_data_update("2023-01-03")
        assert "3 Jan 2023" in result
        assert "03 Jan 2023" not in result

    def test_formats_month_as_abbreviation(self):
        result = generate_last_data_update("2024-12-25")
        assert "Dec" in result

    def test_formats_year_as_four_digits(self):
        result = generate_last_data_update("2024-12-25")
        assert "2024" in result

    def test_different_dates_produce_different_output(self):
        a = generate_last_data_update("2024-01-01")
        b = generate_last_data_update("2025-06-15")
        assert a != b

    def test_raises_on_wrong_format_dashes_missing(self):
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            generate_last_data_update("20260209")

    def test_raises_on_wrong_format_slash_separator(self):
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            generate_last_data_update("09/02/2026")

    def test_raises_on_invalid_month(self):
        with pytest.raises(ValueError):
            generate_last_data_update("2026-13-01")

    def test_raises_on_invalid_day(self):
        with pytest.raises(ValueError):
            generate_last_data_update("2026-02-30")

    def test_raises_on_empty_string(self):
        with pytest.raises(ValueError):
            generate_last_data_update("")

    def test_raises_on_partial_date(self):
        with pytest.raises(ValueError):
            generate_last_data_update("2026-02")

    def test_raises_on_non_date_string(self):
        with pytest.raises(ValueError):
            generate_last_data_update("not-a-date")
