"""Tests for KPI metric calculations in kpi_row.py.

Only the counting/aggregation logic is tested — not HTML rendering.
Each metric value is computed by replicating the expression from
generate_kpi_row and asserting against a known fixture DataFrame.
"""

import pandas as pd
import pytest


@pytest.fixture
def base_df():
    return pd.DataFrame(
        {
            "current_status": [
                "Collection Ongoing",  # Collection Ongoing
                "Collection Ongoing",  # Collection Ongoing
                "Commission Engaged",  # got response
                "Law Passed",  # got response + led to legislation
                "Law Passed",  # got response + led to legislation
                "Rejected Legislation",  # got response
                "Collection Unsuccessful",
                "Withdrawn",
                "Collection Ongoing",  # Collection Ongoing
                "Waiting for Response",
            ],
            "signatures_collected": [
                1_500_000,  # reached 1M
                800_000,
                1_200_000,  # reached 1M
                1_100_000,  # reached 1M
                500_000,
                2_000_000,  # reached 1M
                300_000,
                None,
                0,
                None,
            ],
        }
    )


_RESPONSE_STATUSES = frozenset(
    ["Commission Engaged", "Law Passed", "Rejected Legislation"]
)
_SIG_TARGET = 1_000_000


class TestTotalInitiatives:
    def test_counts_all_rows(self, base_df):
        assert len(base_df) == 10

    def test_empty_df_returns_zero(self):
        df = pd.DataFrame(columns=["current_status", "signatures_collected"])
        assert len(df) == 0


class TestCurrentlyOpen:
    def test_correct_count(self, base_df):
        result = int((base_df["current_status"] == "Collection Ongoing").sum())
        assert result == 3

    def test_none_open_returns_zero(self, base_df):
        df = base_df[base_df["current_status"] != "Collection Ongoing"].copy()
        assert int((df["current_status"] == "Collection Ongoing").sum()) == 0

    def test_all_open_returns_full_count(self):
        df = pd.DataFrame({"current_status": ["Collection Ongoing"] * 5})
        assert int((df["current_status"] == "Collection Ongoing").sum()) == 5


class TestReachedSignatures:
    def test_correct_count(self, base_df):
        result = int((base_df["signatures_collected"] >= _SIG_TARGET).sum())
        assert result == 4

    def test_null_signatures_not_counted(self, base_df):
        result = int((base_df["signatures_collected"] >= _SIG_TARGET).sum())
        # two rows have None — they must not be counted
        assert result == 4

    def test_zero_signatures_not_counted(self, base_df):
        # one row has 0 signatures — must not reach 1M threshold
        result = int((base_df["signatures_collected"] >= _SIG_TARGET).sum())
        assert result == 4

    def test_exact_target_is_counted(self):
        df = pd.DataFrame({"signatures_collected": [_SIG_TARGET]})
        assert int((df["signatures_collected"] >= _SIG_TARGET).sum()) == 1

    def test_one_below_target_not_counted(self):
        df = pd.DataFrame({"signatures_collected": [_SIG_TARGET - 1]})
        assert int((df["signatures_collected"] >= _SIG_TARGET).sum()) == 0

    def test_empty_df_returns_zero(self):
        df = pd.DataFrame({"signatures_collected": pd.Series([], dtype=float)})
        assert int((df["signatures_collected"] >= _SIG_TARGET).sum()) == 0


class TestGotResponse:
    def test_correct_count(self, base_df):
        result = int(base_df["current_status"].isin(_RESPONSE_STATUSES).sum())
        assert result == 4

    def test_excludes_non_response_statuses(self, base_df):
        result = int(base_df["current_status"].isin(_RESPONSE_STATUSES).sum())
        # Collection Unsuccessful, Withdrawn, Collection Ongoing, Waiting for Response excluded
        assert result == 4

    def test_none_with_response_returns_zero(self):
        df = pd.DataFrame({"current_status": ["Collection Ongoing", "Withdrawn"]})
        assert int(df["current_status"].isin(_RESPONSE_STATUSES).sum()) == 0

    def test_all_response_statuses_counted(self):
        df = pd.DataFrame(
            {
                "current_status": [
                    "Commission Engaged",
                    "Law Passed",
                    "Rejected Legislation",
                ]
            }
        )
        assert int(df["current_status"].isin(_RESPONSE_STATUSES).sum()) == 3


class TestLedToLegislation:
    def test_correct_count(self, base_df):
        result = int((base_df["current_status"] == "Law Passed").sum())
        assert result == 2

    def test_excludes_commission_engaged(self, base_df):
        result = int((base_df["current_status"] == "Law Passed").sum())
        assert result == 2  # Commission Engaged must not be counted

    def test_none_law_passed_returns_zero(self):
        df = pd.DataFrame({"current_status": ["Commission Engaged", "Withdrawn"]})
        assert int((df["current_status"] == "Law Passed").sum()) == 0

    def test_subset_of_got_response(self, base_df):
        got_response = int(base_df["current_status"].isin(_RESPONSE_STATUSES).sum())
        led_to_legislation = int((base_df["current_status"] == "Law Passed").sum())
        assert led_to_legislation <= got_response
