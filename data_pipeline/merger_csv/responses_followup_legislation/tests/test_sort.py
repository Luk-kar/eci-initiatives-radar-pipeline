"""
Unit tests for sort.sort_results_by_registration_number.
"""

import pytest

from data_pipeline.merger_csv.responses_followup_legislation.extractor import (
    LegislationResult,
)
from data_pipeline.merger_csv.responses_followup_legislation.sort import (
    sort_results_by_registration_number,
)


def _make(reg: str) -> LegislationResult:
    """Tiny helper — builds a minimal LegislationResult with only the reg number set."""
    return LegislationResult(
        registration_number=reg,
        followup_events=[],
        Law_Passed=None,
        Is_Law_Passed=False,
        Rejected_Legislation=False,
    )


class TestSortResultsByRegistrationNumber:

    def test_orders_results_from_earliest_to_latest_year(self):

        unsorted = [
            _make("2021/000003"),
            _make("2012/000001"),
            _make("2017/000002"),
        ]

        actual = sort_results_by_registration_number(unsorted)

        assert [r.registration_number for r in actual] == [
            "2012/000001",
            "2017/000002",
            "2021/000003",
        ]

    def test_orders_results_within_same_year_by_sequence_number(self):

        unsorted = [
            _make("2019/000010"),
            _make("2019/000002"),
            _make("2019/000001"),
            _make("2019/000003"),
        ]

        actual = sort_results_by_registration_number(unsorted)

        assert [r.registration_number for r in actual] == [
            "2019/000001",
            "2019/000002",
            "2019/000003",
            "2019/000010",
        ]

    def test_does_not_mutate_input_list(self):

        first = _make("2021/000001")
        second = _make("2012/000001")
        unsorted = [first, second]

        sort_results_by_registration_number(unsorted)

        assert unsorted == [first, second]

    def test_returns_new_list_object(self):

        unsorted = [_make("2012/000001")]

        actual = sort_results_by_registration_number(unsorted)

        assert actual is not unsorted

    def test_returns_empty_list_for_empty_input(self):

        assert sort_results_by_registration_number([]) == []

    def test_returns_single_item_unchanged(self):

        only = _make("2018/000005")

        actual = sort_results_by_registration_number([only])

        assert [r.registration_number for r in actual] == ["2018/000005"]

    def test_is_stable_for_duplicate_registration_numbers(self):
        """
        Duplicate registration numbers should never appear in real data, but
        we still want a deterministic, stable ordering if they do.
        """
        first = _make("2015/000001")
        second = _make("2015/000001")

        actual = sort_results_by_registration_number([first, second])

        assert actual[0] is first
        assert actual[1] is second
