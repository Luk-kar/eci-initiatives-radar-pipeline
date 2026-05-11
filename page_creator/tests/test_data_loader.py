import re
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from page_creator.data_loader import find_latest_csv


def make_csv(path: Path, content: str = "col") -> Path:
    path.write_text(content, encoding="utf-8")
    return path


class TestFindLatestCsv:
    @pytest.fixture
    def mock_newest_run_dir(self, tmp_path):

        with patch(
            "page_creator.data_loader.find_newest_scraped_data_dir",
            return_value=tmp_path,
        ) as mock:
            yield mock

    def _make_dashboard_csv(self, tmp_path, timestamp, content="col\nval\n"):

        return make_csv(tmp_path / f"eci_dashboard_{timestamp}.csv", content)

    def test_returns_path_and_date(self, tmp_path, mock_newest_run_dir):

        self._make_dashboard_csv(tmp_path, "2025-06-01_10-00-00")
        path, date = find_latest_csv()

        assert isinstance(path, Path)
        assert path.name == "eci_dashboard_2025-06-01_10-00-00.csv"
        assert date == "2025-06-01"

    def test_returns_most_recent_by_timestamp(self, tmp_path, mock_newest_run_dir):

        self._make_dashboard_csv(tmp_path, "2024-01-01_08-00-00")
        self._make_dashboard_csv(tmp_path, "2025-06-15_12-30-00")
        self._make_dashboard_csv(tmp_path, "2023-12-31_23-59-59")
        _, date = find_latest_csv()

        assert date == "2025-06-15"

    def test_skips_files_without_valid_timestamp(self, tmp_path, mock_newest_run_dir):

        make_csv(tmp_path / "eci_dashboard_backup.csv")
        self._make_dashboard_csv(tmp_path, "2025-03-10_09-00-00")
        _, date = find_latest_csv()

        assert date == "2025-03-10"

    def test_raises_if_data_dir_missing(self, mock_newest_run_dir):

        mock_newest_run_dir.side_effect = FileNotFoundError("Data directory not found")

        with pytest.raises(FileNotFoundError, match="Data directory not found"):
            find_latest_csv()

    def test_raises_if_no_csv_files(self, tmp_path, mock_newest_run_dir):

        # Fix: Replaced `\\*` with `\*` so it parses exactly one backslash before the asterisk
        with pytest.raises(
            FileNotFoundError, match=r"No 'eci_dashboard_\*\.csv' files found"
        ):
            find_latest_csv()

    def test_raises_if_only_malformed_timestamps(self, tmp_path, mock_newest_run_dir):

        make_csv(tmp_path / "eci_dashboard_backup.csv")
        make_csv(tmp_path / "eci_dashboard_bad-date.csv")

        with pytest.raises(ValueError, match="Expected pattern"):
            find_latest_csv()

    def test_raises_on_corrupted_csv(self, tmp_path, mock_newest_run_dir):

        bad = tmp_path / "eci_dashboard_2025-05-01_10-00-00.csv"
        # Fix: Replaced `\\x` with `\x` so it generates actual binary bytes
        bad.write_bytes(b"\x00\xff\xfe" * 100)

        with pytest.raises(ValueError, match="corrupted"):
            find_latest_csv()

    def test_raises_on_newest_corrupted_with_no_fallback(
        self, tmp_path, mock_newest_run_dir
    ):
        bad = tmp_path / "eci_dashboard_2026-01-01_00-00-00.csv"
        # Fix: Replaced `\\x` with `\x` so it generates actual binary bytes
        bad.write_bytes(b"\x00\xff\xfe" * 100)
        self._make_dashboard_csv(tmp_path, "2025-06-01_10-00-00")

        with pytest.raises(ValueError, match="corrupted"):
            find_latest_csv()

    def test_returned_path_exists(self, tmp_path, mock_newest_run_dir):

        self._make_dashboard_csv(tmp_path, "2025-09-20_14-00-00")
        path, _ = find_latest_csv()

        assert path.exists()

    def test_date_format_is_yyyy_mm_dd(self, tmp_path, mock_newest_run_dir):

        self._make_dashboard_csv(tmp_path, "2024-11-30_08-45-00")
        _, date = find_latest_csv()

        # Fix: Replaced `\\d` with `\d` to correctly match digit regex
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", date)
