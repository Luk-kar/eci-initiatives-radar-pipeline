"""Unit tests for pipeline_shared.sort.sort_by_registration_number."""

from dataclasses import dataclass

from ..sort import (
    sort_by_registration_number,
)


@dataclass
class _Row:
    registration_number: str
    payload: str = ""


class TestSortResultsByRegistrationNumber:

    def test_orders_dataclass_rows_across_years(self) -> None:
        unsorted = [
            _Row("2021/000003"),
            _Row("2012/000001"),
            _Row("2017/000002"),
        ]
        actual = sort_by_registration_number(unsorted)
        assert [r.registration_number for r in actual] == [
            "2012/000001",
            "2017/000002",
            "2021/000003",
        ]

    def test_orders_dict_rows_within_same_year(self) -> None:
        unsorted = [
            {"registration_number": "2019/000010"},
            {"registration_number": "2019/000002"},
            {"registration_number": "2019/000001"},
            {"registration_number": "2019/000003"},
        ]
        actual = sort_by_registration_number(unsorted)
        assert [r["registration_number"] for r in actual] == [
            "2019/000001",
            "2019/000002",
            "2019/000003",
            "2019/000010",
        ]

    def test_does_not_mutate_input_list(self) -> None:
        first, second = _Row("2021/000001"), _Row("2012/000001")
        unsorted = [first, second]
        sort_by_registration_number(unsorted)
        assert unsorted == [first, second]

    def test_returns_new_list_object(self) -> None:
        unsorted = [_Row("2012/000001")]
        assert sort_by_registration_number(unsorted) is not unsorted

    def test_returns_empty_list_for_empty_input(self) -> None:
        assert sort_by_registration_number([]) == []

    def test_is_stable_for_duplicate_registration_numbers(self) -> None:
        first, second = _Row("2015/000001", "a"), _Row("2015/000001", "b")
        actual = sort_by_registration_number([first, second])
        assert actual[0] is first
        assert actual[1] is second

    def test_accepts_any_iterable(self) -> None:
        gen = (_Row(r) for r in ("2020/000002", "2018/000001"))
        actual = sort_by_registration_number(gen)
        assert [r.registration_number for r in actual] == [
            "2018/000001",
            "2020/000002",
        ]
