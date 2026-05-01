import csv
from pathlib import Path

from data_pipeline.merger_csv.responses_followup_legislation import write


class _FakeNow:
    def strftime(self, fmt: str) -> str:
        return "2026-04-24_13-53-00"


class _FakeDateTime:
    @staticmethod
    def now():
        return _FakeNow()


class TestWriteOutput:
    def test_write_output_creates_csv_with_expected_rows(
        self,
        monkeypatch,
        tmp_path: Path,
        legislation_results,
    ):
        monkeypatch.setattr(write, "datetime", _FakeDateTime)
        monkeypatch.setattr(
            write,
            "ECI_RESPONSES_FOLLOWUP_LEGISLATION_PATTERN",
            "eci_responses_followup_legislation_{timestamp}.csv",
        )

        output_path = write.write_output(tmp_path, legislation_results)

        assert output_path == (
            tmp_path / "eci_responses_followup_legislation_2026-04-24_13-53-00.csv"
        )
        assert output_path.exists()

        with output_path.open(encoding="utf-8", newline="") as fh:
            reader = csv.reader(fh)
            header = next(reader)
            rows = [dict(zip(header, row)) for row in reader]

        assert header == [
            "registration_number",
            "commission_answer",
            "followup_events",
            "law_passed",
            "Is_Law_Passed",
            "Rejected_Legislation",
        ]

        assert len(rows) == 2

        # Row 0
        assert rows[0]["registration_number"] == "2012/000001"
        assert rows[0]["commission_answer"] == (
            "['Commission answer 1', 'Commission answer 2']"
        )
        assert rows[0]["followup_events"] == "['Follow-up 1', 'Follow-up 2']"
        assert rows[0]["law_passed"] == "['Follow-up 1']"
        assert rows[0]["Is_Law_Passed"] == "True"
        assert rows[0]["Rejected_Legislation"] == "False"

        # Row 1
        assert rows[1]["registration_number"] == "2012/000002"
        assert rows[1]["commission_answer"] == "['Commission answer 3']"
        assert rows[1]["followup_events"] == "['Follow-up 3']"
        assert rows[1]["law_passed"] == ""
        assert rows[1]["Is_Law_Passed"] == "False"
        assert rows[1]["Rejected_Legislation"] == "True"
