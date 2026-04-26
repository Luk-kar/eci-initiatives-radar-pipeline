"""
Tests that responses_followup.extractor.run() sorts records by
registration_number between build_records and write_csv.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch
from typing import get_args, get_origin

import pytest

from data_pipeline.extractor.responses_followup import extractor as extractor_module
from data_pipeline.extractor.responses_followup.model import (
    ECIFollowupRecord,
)


from typing import get_args, get_origin


def _placeholder_for(annotation: object) -> object:
    """Return a benign value matching *annotation*'s type — only used to satisfy
    pydantic validation in tests where the field value is irrelevant."""

    origin = get_origin(annotation)

    if origin in (list, list):
        return []
    if origin is dict:
        return {}
    if origin in (tuple,):
        return ()

    # Optional[X] / Union[..., None] → use the first non-None arg.
    if origin is not None and type(None) in get_args(annotation):

        non_none = [a for a in get_args(annotation) if a is not type(None)]

        if non_none:
            return _placeholder_for(non_none[0])

        return None

    if annotation is str:
        return ""
    if annotation is int:
        return 0
    if annotation is float:
        return 0.0
    if annotation is bool:
        return False

    return None


def _record(reg: str) -> ECIFollowupRecord:
    """Build a minimal ECIFollowupRecord — only registration_number matters
    for these tests; every other field gets a type-appropriate placeholder."""

    values = {}

    for name, info in ECIFollowupRecord.model_fields.items():

        if name == "registration_number":
            values[name] = reg
        else:
            values[name] = _placeholder_for(info.annotation)

    return ECIFollowupRecord(**values)


@pytest.fixture
def stubbed_pipeline(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):

    html_dir = tmp_path / "html"
    output_csv = tmp_path / "out.csv"
    responses_csv = tmp_path / "eci_responses.csv"
    logger = MagicMock(name="step_logger")

    monkeypatch.setattr(
        extractor_module,
        "setup",
        lambda *_a, **_kw: (html_dir, output_csv, responses_csv, logger),
    )
    monkeypatch.setattr(extractor_module, "collect_html_files", lambda _d: {})
    monkeypatch.setattr(extractor_module, "load_metadata", lambda *_a: {})
    monkeypatch.setattr(extractor_module, "parse_html_files", lambda *_a: {})

    unsorted_records = [
        _record("2021/000003"),
        _record("2012/000001"),
        _record("2017/000002"),
    ]
    monkeypatch.setattr(
        extractor_module, "build_records", lambda *_a, **_kw: list(unsorted_records)
    )

    write_calls: list[list[ECIFollowupRecord]] = []

    def fake_write(records, _csv):
        write_calls.append(list(records))

    monkeypatch.setattr(extractor_module, "write_csv", fake_write)

    return {
        "output_csv": output_csv,
        "write_calls": write_calls,
        "unsorted_records": unsorted_records,
    }


class TestResponsesFollowupRunSorting:

    def test_run_passes_records_sorted_by_registration_number_to_writer(
        self, stubbed_pipeline
    ):

        extractor_module.run(
            "eci_responses_followup_2026-04-24_10-00-00.csv",
            "2026-04-24_10-00-00",
        )

        written = stubbed_pipeline["write_calls"]
        assert len(written) == 1
        assert [r.registration_number for r in written[0]] == [
            "2012/000001",
            "2017/000002",
            "2021/000003",
        ]

    def test_run_invokes_shared_sort_helper(self, stubbed_pipeline):

        with patch.object(
            extractor_module,
            "sort_by_registration_number",
            wraps=extractor_module.sort_by_registration_number,
        ) as sort_spy:
            extractor_module.run(
                "eci_responses_followup_2026-04-24_10-00-00.csv",
                "2026-04-24_10-00-00",
            )

        sort_spy.assert_called_once()
        passed = sort_spy.call_args.args[0]
        assert [r.registration_number for r in passed] == [
            "2021/000003",
            "2012/000001",
            "2017/000002",
        ]

    def test_run_does_not_mutate_records_returned_by_build_records(
        self, stubbed_pipeline
    ):

        extractor_module.run(
            "eci_responses_followup_2026-04-24_10-00-00.csv",
            "2026-04-24_10-00-00",
        )

        assert [
            r.registration_number for r in stubbed_pipeline["unsorted_records"]
        ] == ["2021/000003", "2012/000001", "2017/000002"]
