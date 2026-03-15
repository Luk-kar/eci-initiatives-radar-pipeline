"""Tests for data logic in outcomes.py — normalisation, counting, ordering."""

import pytest
import pandas as pd

from page_creator.partials.charts.outcomes import (
    _normalise_statuses,
    _build_counts,
    _truncate_title,
    STATUS_COLORS,
    _LABEL_ALIASES,
)


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Law Passed",
                "Law Passed",
                "Commission Engaged",
                "Rejected Legislation",
                "Rejected Legislation",
                "Rejected Legislation",
                "Waiting for Response",  # aliased → Awaiting Response
                "Collection Ongoing",
                "Collection Unsuccessful",
                "Withdrawn",
            ],
            "title": [f"ECI {i}" for i in range(10)],
        }
    )


class TestNormaliseStatuses:
    def test_waiting_for_response_aliased(self, base_df):

        result = _normalise_statuses(base_df)
        assert "Waiting for Response" not in result["current_status"].values
        assert "Awaiting Response" in result["current_status"].values

    def test_known_statuses_unchanged(self, base_df):

        result = _normalise_statuses(base_df)
        for status in ["Law Passed", "Commission Engaged", "Rejected Legislation"]:
            assert status in result["current_status"].values

    def test_unknown_status_raises_value_error(self, base_df):

        bad_df = base_df.copy()
        bad_df.loc[0, "current_status"] = "Totally Unknown Status"
        with pytest.raises(ValueError, match="Unrecognised status values"):
            _normalise_statuses(bad_df)

    def test_does_not_mutate_original(self, base_df):

        original = base_df["current_status"].tolist()
        _normalise_statuses(base_df)
        assert base_df["current_status"].tolist() == original

    def test_all_aliases_map_correctly(self):

        df = pd.DataFrame(
            {
                "current_status": list(_LABEL_ALIASES.keys()),
                "title": ["T"] * len(_LABEL_ALIASES),
            }
        )
        result = _normalise_statuses(df)
        for aliased in _LABEL_ALIASES.values():
            assert aliased in result["current_status"].values


class TestBuildCounts:
    def test_correct_counts(self, base_df):

        df = _normalise_statuses(base_df)
        counts = _build_counts(df)
        assert (
            counts.loc[counts["current_status"] == "Law Passed", "count"].iloc[0] == 2
        )
        assert (
            counts.loc[
                counts["current_status"] == "Rejected Legislation", "count"
            ].iloc[0]
            == 3
        )

    def test_percentage_sums_to_100(self, base_df):

        df = _normalise_statuses(base_df)
        counts = _build_counts(df)
        assert abs(counts["percentage"].sum() - 100.0) < 0.2

    def test_color_column_present_and_non_empty(self, base_df):

        df = _normalise_statuses(base_df)
        counts = _build_counts(df)
        assert counts["color"].notna().all()
        assert all(counts["color"].str.startswith("#"))

    def test_status_order_matches_status_colors(self, base_df):

        df = _normalise_statuses(base_df)
        counts = _build_counts(df)
        order = list(STATUS_COLORS.keys())
        indices = [order.index(s) for s in counts["current_status"] if s in order]
        assert indices == sorted(indices)

    def test_eci_list_column_present(self, base_df):

        df = _normalise_statuses(base_df)
        counts = _build_counts(df)
        assert "eci_list" in counts.columns


class TestTruncateTitle:
    def test_short_title_unchanged(self):
        assert _truncate_title("Short") == "Short"

    def test_long_title_truncated_with_ellipsis(self):

        title = "A" * 50
        result = _truncate_title(title)
        assert result.endswith("…")
        assert len(result) == 40

    def test_exact_max_length_unchanged(self):

        title = "A" * 40
        assert _truncate_title(title) == title

    def test_custom_max_len(self):
        result = _truncate_title("Hello World", max_len=5)
        assert result == "Hell…"
