import csv
import logging
import shutil
from pathlib import Path

import pytest

from data_pipeline.merger_csv.responses_followup_legislation import __main__ as main_module
from data_pipeline.merger_csv.responses_followup_legislation import write as write_module


FIXTURES_DIR = Path(__file__).parent / "fixtures"


class _FrozenNow:
    def strftime(self, fmt: str) -> str:
        return "2026-04-24_13-50-24"


class _FrozenDateTime:
    @staticmethod
    def now():
        return _FrozenNow()


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


@pytest.fixture
def synthetic_legislation_csv_fixture_dir(tmp_path: Path) -> dict[str, Path]:

    responses_src = FIXTURES_DIR / "eci_responses_2026-04-24_10-00-00.csv"
    followup_src = FIXTURES_DIR / "eci_responses_followup_2026-04-24_10-00-00.csv"
    expected_src = (
        FIXTURES_DIR
        / "expected_eci_responses_followup_legislation_2026-04-24_13-50-24.csv"
    )

    responses_dst = tmp_path / responses_src.name
    followup_dst = tmp_path / followup_src.name

    shutil.copyfile(responses_src, responses_dst)
    shutil.copyfile(followup_src, followup_dst)

    return {
        "data_dir": tmp_path,
        "expected_output": expected_src,
    }


class TestResponsesFollowupLegislationMainEndToEnd:
    def test_main_writes_expected_csv_for_synthetic_fixture_files(
        self,
        monkeypatch: pytest.MonkeyPatch,
        synthetic_legislation_csv_fixture_dir: dict[str, Path],
    ):
        """
        Verify that the CLI entry point produces the expected legislation CSV
        from synthetic response and follow-up fixture files.
        """
        
        data_dir = synthetic_legislation_csv_fixture_dir["data_dir"]
        expected_output = synthetic_legislation_csv_fixture_dir["expected_output"]

        monkeypatch.setattr(
            main_module,
            "find_newest_scraped_data_dir",
            lambda *args, **kwargs: data_dir,
        )
        monkeypatch.setattr(
            main_module,
            "get_logger",
            lambda *args, **kwargs: logging.getLogger("test_legislation_e2e"),
        )
        monkeypatch.setattr(write_module, "datetime", _FrozenDateTime)

        main_module.main()

        actual_output = (
            data_dir / "eci_responses_followup_legislation_2026-04-24_13-50-24.csv"
        )

        assert actual_output.exists()

        actual_rows = _read_csv_rows(actual_output)
        expected_rows = _read_csv_rows(expected_output)

        assert actual_rows == expected_rows