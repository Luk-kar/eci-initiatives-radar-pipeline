"""
Tests that responses.extractor.run() sorts records by registration_number
between build_records and write_csv.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from data_pipeline.extractor.responses import extractor as extractor_module
from data_pipeline.extractor.responses.model import ECIResponseRecord


def _record(reg: str) -> ECIResponseRecord:
    return ECIResponseRecord(
        registration_number=reg,
        title=f"Title {reg}",
        initiative_url=f"https://example.test/{reg}",
        response_url=f"https://example.test/r/{reg}",
        commission_answer=None,
        followup_additional_website=None,
        followup_events=None,
    )


@pytest.fixture
def stubbed_pipeline(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Stub every side-effecting step so only the sort wiring is exercised."""

    html_dir = tmp_path / "html"
    output_csv = tmp_path / "out.csv"
    initiatives_csv = tmp_path / "initiatives.csv"
    logger = MagicMock(name="step_logger")

    monkeypatch.setattr(
        extractor_module,
        "setup",
        lambda *_a, **_kw: (html_dir, output_csv, initiatives_csv, logger),
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

    write_calls: list[list[ECIResponseRecord]] = []

    def fake_write(records, _csv):
        write_calls.append(list(records))

    monkeypatch.setattr(extractor_module, "write_csv", fake_write)

    return {
        "output_csv": output_csv,
        "write_calls": write_calls,
        "unsorted_records": unsorted_records,
    }


class TestResponsesRunSorting:

    def test_run_passes_records_sorted_by_registration_number_to_writer(
        self, stubbed_pipeline
    ):

        extractor_module.run(
            "eci_responses_2026-04-24_10-00-00.csv", "2026-04-24_10-00-00"
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
                "eci_responses_2026-04-24_10-00-00.csv", "2026-04-24_10-00-00"
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
            "eci_responses_2026-04-24_10-00-00.csv", "2026-04-24_10-00-00"
        )

        assert [
            r.registration_number for r in stubbed_pipeline["unsorted_records"]
        ] == [
            "2021/000003",
            "2012/000001",
            "2017/000002",
        ]
