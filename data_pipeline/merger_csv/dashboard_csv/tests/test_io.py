"""Tests for data_pipeline.merger_csv.dashboard_csv.io."""

import csv
import re
from pathlib import Path

import pytest

from data_pipeline.merger_csv.dashboard_csv.io import (
    filter_columns,
    find_latest_csv,
    find_latest_data_dir,
    load_csv,
    validate_csv_exists,
)
from data_pipeline.pipeline_shared.consts import FILE_ENCODING


class TestFindLatestDataDir:
    """Tests for run-directory resolution."""

    def test_finds_latest_chronological_dir(self, tmp_path):
        """It should return the lexicographically last timestamped directory."""

        dir1 = tmp_path / "2024-01-01_10-00-00"
        dir2 = tmp_path / "2024-01-01_12-00-00"
        dir3 = tmp_path / "2024-01-01_11-00-00"

        for d in (dir1, dir2, dir3):
            d.mkdir()

        latest = find_latest_data_dir(tmp_path)
        assert latest.name == "2024-01-01_12-00-00"

    def test_ignores_non_timestamp_dirs(self, tmp_path):
        """It should ignore directories that don't match the timestamp pattern."""

        valid_dir = tmp_path / "2024-01-01_10-00-00"
        valid_dir.mkdir()

        invalid_dir = tmp_path / "invalid-name"
        invalid_dir.mkdir()

        (tmp_path / "2024-01-01_10-00-00.txt").touch()  # Valid name, but a file

        latest = find_latest_data_dir(tmp_path)
        assert latest == valid_dir

    def test_raises_when_no_dirs_found(self, tmp_path):
        """It should raise FileNotFoundError if no matching directories exist."""

        with pytest.raises(
            FileNotFoundError, match="No timestamped run directories found under"
        ):
            find_latest_data_dir(tmp_path)


class TestFindLatestCsv:
    """Tests for resolving the latest CSV within a run directory."""

    def test_finds_latest_glob_match(self, tmp_path):
        """It should return the lexicographically latest file matching the glob."""

        (tmp_path / "eci_initiatives_1.csv").touch()
        (tmp_path / "eci_initiatives_3.csv").touch()
        (tmp_path / "eci_initiatives_2.csv").touch()
        (tmp_path / "other_file.csv").touch()

        latest = find_latest_csv(tmp_path, "eci_initiatives_*.csv")
        assert latest.name == "eci_initiatives_3.csv"

    def test_raises_when_no_matches(self, tmp_path):
        """It should raise FileNotFoundError if the glob matches nothing."""

        with pytest.raises(FileNotFoundError, match="No files matching"):
            find_latest_csv(tmp_path, "missing_*.csv")


class TestValidateCsvExists:
    """Tests for verifying CSV files exist and have data rows."""

    def test_validates_healthy_csv(self, tmp_path):
        """It should return silently for a valid CSV with a header and data."""

        csv_path = tmp_path / "test.csv"
        csv_path.write_text("header1,header2\nval1,val2\n", encoding=FILE_ENCODING)

        validate_csv_exists(csv_path)  # Should not raise

    def test_raises_missing_file(self, tmp_path):
        """It should raise FileNotFoundError for missing files."""

        csv_path = tmp_path / "missing.csv"

        with pytest.raises(FileNotFoundError, match="Required CSV does not exist"):
            validate_csv_exists(csv_path)

    def test_raises_directory(self, tmp_path):
        """It should raise FileNotFoundError if the path is a directory."""

        csv_path = tmp_path / "dir.csv"
        csv_path.mkdir()

        with pytest.raises(
            FileNotFoundError, match="Expected a regular file but found"
        ):
            validate_csv_exists(csv_path)

    def test_raises_empty_file(self, tmp_path):
        """It should raise ValueError for completely empty files."""

        csv_path = tmp_path / "empty.csv"
        csv_path.write_text("", encoding=FILE_ENCODING)

        with pytest.raises(ValueError, match="CSV file is completely empty"):
            validate_csv_exists(csv_path)

    def test_raises_header_only(self, tmp_path):
        """It should raise ValueError for files with a header but no data."""

        csv_path = tmp_path / "header_only.csv"
        csv_path.write_text("header1,header2\n", encoding=FILE_ENCODING)

        with pytest.raises(ValueError, match="CSV file contains no data rows"):
            validate_csv_exists(csv_path)


class TestLoadCsv:
    """Tests for loading CSV into dictionary rows."""

    def test_loads_rows(self, tmp_path):
        """It should return a list of dicts reflecting the CSV content."""

        csv_path = tmp_path / "test.csv"
        csv_path.write_text("a,b\n1,2\n3,4\n", encoding=FILE_ENCODING)

        rows = load_csv(csv_path)
        assert len(rows) == 2
        assert rows[0] == {"a": "1", "b": "2"}
        assert rows[1] == {"a": "3", "b": "4"}


class TestFilterColumns:
    """Tests for column projection/filtering."""

    def test_keeps_specified_columns(self):
        """It should return only the columns listed in `keep`."""

        rows = [
            {"a": "1", "b": "2", "c": "3"},
            {"a": "4", "b": "5", "c": "6"},
        ]

        filtered = filter_columns(rows, ("a", "c"), source_label="test")

        assert len(filtered) == 2
        assert filtered[0] == {"a": "1", "c": "3"}
        assert filtered[1] == {"a": "4", "c": "6"}

    def test_coerces_missing_values_to_empty_strings(self):
        """It should replace None values with empty strings."""

        rows = [
            {"a": "1", "b": None},
        ]

        filtered = filter_columns(rows, ("a", "b"), source_label="test")

        assert filtered[0] == {"a": "1", "b": ""}

    def test_returns_empty_list_for_empty_input(self):
        """It should return an empty list if rows is empty."""

        assert filter_columns([], ("a", "b"), source_label="test") == []

    def test_raises_when_required_column_missing_from_header(self):
        """It should raise ValueError if a requested column is missing entirely."""

        rows = [
            {"a": "1", "b": "2"},
        ]

        with pytest.raises(
            ValueError, match="missing required column\\(s\\) \\['c'\\]"
        ):
            filter_columns(rows, ("a", "c"), source_label="test_source")
