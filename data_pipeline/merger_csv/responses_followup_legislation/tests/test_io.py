from pathlib import Path

import pytest

from data_pipeline.merger_csv.responses_followup_legislation import io


class TestFindLatestCsv:
    def test_find_latest_csv_returns_lexicographically_latest_match(self, tmp_path: Path):

        older = tmp_path / "eci_responses_2026-04-23_18-18-51.csv"
        newer = tmp_path / "eci_responses_2026-04-24_11-31-22.csv"

        older.write_text("a,b\n1,2\n", encoding="utf-8")
        newer.write_text("a,b\n3,4\n", encoding="utf-8")

        actual = io.find_latest_csv(tmp_path, "eci_responses_*.csv")

        assert actual == newer

    def test_find_latest_csv_raises_when_no_match_exists(self, tmp_path: Path):

        with pytest.raises(FileNotFoundError, match="No files matching"):
            io.find_latest_csv(tmp_path, "eci_responses_*.csv")


class TestValidateCsvExists:
    def test_validate_csv_exists_accepts_csv_with_header_and_data_row(self, tmp_path: Path):

        path = tmp_path / "valid.csv"
        path.write_text("col1,col2\n1,2\n", encoding="utf-8")

        io.validate_csv_exists(path)

    def test_validate_csv_exists_raises_for_missing_file(self, tmp_path: Path):

        path = tmp_path / "missing.csv"

        with pytest.raises(FileNotFoundError, match="does not exist"):
            io.validate_csv_exists(path)

    def test_validate_csv_exists_raises_when_path_is_not_a_file(self, tmp_path: Path):

        with pytest.raises(FileNotFoundError, match="Expected a regular file"):
            io.validate_csv_exists(tmp_path)

    def test_validate_csv_exists_raises_for_empty_file(self, tmp_path: Path):

        path = tmp_path / "empty.csv"
        path.write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="completely empty"):
            io.validate_csv_exists(path)

    def test_validate_csv_exists_raises_for_header_only_file(self, tmp_path: Path):

        path = tmp_path / "header_only.csv"
        path.write_text("col1,col2\n", encoding="utf-8")

        with pytest.raises(ValueError, match="contains no data rows"):
            io.validate_csv_exists(path)


class TestLoadCsv:
    def test_load_csv_returns_rows_from_csv(self, tmp_path: Path):
        path = tmp_path / "rows.csv"
        path.write_text(
            "registration_number,commission_answer_text\n"
            "2012/000001,\"['Answer 1']\"\n",
            encoding="utf-8",
        )

        actual = io.load_csv(path)

        assert actual == [
            {
                "registration_number": "2012/000001",
                "commission_answer_text": "['Answer 1']",
            }
        ]