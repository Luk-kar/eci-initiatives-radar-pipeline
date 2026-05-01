"""Tests for data_pipeline.merger_csv.dashboard_csv.run."""

import csv
import logging
import shutil
from pathlib import Path

import pytest

from data_pipeline.merger_csv.dashboard_csv import (
    __main__ as main_module,
)
from data_pipeline.merger_csv.dashboard_csv import (
    run as run_module,
)
from data_pipeline.merger_csv.dashboard_csv import (
    session as session_module,
)
from data_pipeline.merger_csv.dashboard_csv import (
    write as write_module,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class _FrozenNow:
    def strftime(self, fmt: str) -> str:
        return "2026-05-01_12-00-00"


class _FrozenDateTime:
    @staticmethod
    def now():
        return _FrozenNow()


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


@pytest.fixture
def real_dashboard_csv_fixture_dir(tmp_path: Path) -> dict[str, Path]:
    """
    Provide a run directory with the three required source files populated
    by real data fixtures from the `fixtures` directory.
    """
    # Assuming you placed subsets of the real files in the fixtures directory.
    # We copy them to tmp_path to ensure the test runner doesn't mutate fixtures
    # or leave outputs behind in the repo.
    initiatives_src = FIXTURES_DIR / "eci_initiatives_2026-04-26_17-44-50.csv"
    responses_src = FIXTURES_DIR / "eci_responses_2026-04-26_17-53-28.csv"
    legislation_src = (
        FIXTURES_DIR / "eci_responses_followup_legislation_2026-04-26_14-26-29.csv"
    )
    expected_src = FIXTURES_DIR / "expected_eci_dashboard_2026-05-01_12-00-00.csv"

    # We copy them into tmp_path so the data pipeline operates inside the temporary directory
    initiatives_dst = tmp_path / initiatives_src.name
    responses_dst = tmp_path / responses_src.name
    legislation_dst = tmp_path / legislation_src.name

    shutil.copyfile(initiatives_src, initiatives_dst)
    shutil.copyfile(responses_src, responses_dst)
    shutil.copyfile(legislation_src, legislation_dst)

    return {
        "data_dir": tmp_path,
        "expected_output": expected_src,
    }


class TestDashboardCsvMainEndToEnd:
    def test_main_writes_expected_csv_for_real_fixture_files(
        self,
        monkeypatch: pytest.MonkeyPatch,
        real_dashboard_csv_fixture_dir: dict[str, Path],
    ):
        """
        Verify that the CLI entry point produces the expected dashboard CSV
        from real response and followup fixture files.
        """

        data_dir = real_dashboard_csv_fixture_dir["data_dir"]
        expected_output = real_dashboard_csv_fixture_dir["expected_output"]

        # 1. Patch the directory locator to return our temporary dir
        monkeypatch.setattr(
            session_module,
            "find_latest_data_dir",
            lambda *args, **kwargs: data_dir,
        )

        # 2. Patch the logger to suppress output
        monkeypatch.setattr(
            session_module,
            "get_logger",
            lambda *args, **kwargs: logging.getLogger("test_dashboard_e2e"),
        )

        # 3. Freeze datetime so the output filename matches our expectation
        monkeypatch.setattr(write_module, "datetime", _FrozenDateTime)

        # 4. Run the actual pipeline
        main_module.run()

        # 5. Locate output
        actual_output = data_dir / "eci_dashboard_2026-05-01_12-00-00.csv"

        assert actual_output.exists()

        actual_rows = _read_csv_rows(actual_output)
        expected_rows = _read_csv_rows(expected_output)

        assert actual_rows == expected_rows

    def test_main_invokes_sort_and_writes_rows_in_registration_number_order(
        self,
        monkeypatch: pytest.MonkeyPatch,
        real_dashboard_csv_fixture_dir: dict[str, Path],
    ):
        """
        Verify the pipeline:
          - actually invokes the registration-number proxy sort step, and
          - writes its rows in ascending chronological order.
        """

        data_dir = real_dashboard_csv_fixture_dir["data_dir"]

        monkeypatch.setattr(
            session_module,
            "find_latest_data_dir",
            lambda *args, **kwargs: data_dir,
        )
        monkeypatch.setattr(
            session_module,
            "get_logger",
            lambda *args, **kwargs: logging.getLogger("test_dashboard_e2e_sort"),
        )
        monkeypatch.setattr(write_module, "datetime", _FrozenDateTime)

        captured: dict[str, list] = {"input": [], "output": []}
        original_sort = run_module.sort_by_registration_number

        def spy_sort(results):
            captured["input"] = list(results)
            sorted_results = original_sort(results)
            captured["output"] = list(sorted_results)
            return sorted_results

        # Patch the sort helper where it is imported in run.py
        monkeypatch.setattr(run_module, "sort_by_registration_number", spy_sort)

        # Run pipeline
        main_module.run()

        # Sort was invoked with non-empty input.
        assert captured["input"], "sort_by_registration_number was not called"

        # Sort produced ascending order (testing that the output proxy sorts correctly).
        sorted_regs = [r.registration_number for r in captured["output"]]
        assert sorted_regs == sorted(sorted_regs)

        # The CSV reflects the order produced by the sort step.
        actual_output = data_dir / "eci_dashboard_2026-05-01_12-00-00.csv"
        actual_rows = _read_csv_rows(actual_output)
        assert [row["registration_number"] for row in actual_rows] == sorted_regs
