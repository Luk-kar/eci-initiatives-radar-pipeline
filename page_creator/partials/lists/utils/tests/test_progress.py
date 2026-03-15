"""Tests for progress_bar in utils/progress.py."""

import pytest
from page_creator.partials.lists.utils.progress import progress_bar


class TestProgressBar:
    def test_returns_html_string(self):

        assert isinstance(progress_bar(50.0), str)

    def test_contains_progress_bar_class(self):

        assert 'class="progress-bar"' in progress_bar(50.0)

    def test_fill_width_reflects_percentage(self):

        result = progress_bar(75.0)
        assert 'style="width:75.0%"' in result

    def test_zero_percent(self):

        assert 'style="width:0.0%"' in progress_bar(0.0)

    def test_100_percent(self):

        assert 'style="width:100.0%"' in progress_bar(100.0)

    def test_over_100_clamped_to_100_visually(self):

        result = progress_bar(150.0)
        assert 'style="width:100.0%"' in result

    def test_over_100_adds_over_class(self):

        assert "progress-bar__fill--over" in progress_bar(150.0)

    def test_exactly_100_does_not_add_over_class(self):

        assert "progress-bar__fill--over" not in progress_bar(100.0)

    def test_negative_clamped_to_zero(self):

        assert 'style="width:0.0%"' in progress_bar(-10.0)

    def test_modifier_class_added(self):

        result = progress_bar(50.0, "signatures")
        assert "progress-bar__fill--signatures" in result

    def test_no_modifier_no_extra_class(self):

        result = progress_bar(50.0)
        assert "progress-bar__fill--" not in result

    def test_modifier_and_over_both_applied(self):

        result = progress_bar(200.0, "days-left")
        assert "progress-bar__fill--days-left" in result
        assert "progress-bar__fill--over" in result
