"""Tests for responses.extractor.collect."""

from pathlib import Path
from unittest.mock import patch

import pytest

from data_pipeline.extractor.responses.extractor.collect import (
    collect_html_files,
    _scan_html_files,
)

# Redefined here instead of imported from FilePatterns to decouple collect tests
# from the shared constant — if FilePatterns.FILENAME_REGEX ever changes, these
# tests will still verify the behaviour that collect.py was written against,
# making the regression explicit rather than silently inheriting the new pattern.
FILENAME_REGEX = r"^(\d{4})_(\d+)\.html$"


def _create_html_file(base: Path, subdir: str, name: str) -> Path:

    directory = base / subdir
    directory.mkdir(parents=True, exist_ok=True)
    file = directory / name
    file.write_text("<html/>")

    return file


class TestCollectHtmlFiles:

    def test_returns_correct_mapping(self, tmp_path):

        _create_html_file(tmp_path, "2020", "2020_000001.html")
        _create_html_file(tmp_path, "2021", "2021_000002.html")

        with patch(
            "data_pipeline.extractor.responses.extractor.collect.FilePatterns.FILENAME_REGEX",
            FILENAME_REGEX,
        ):

            result = collect_html_files(tmp_path)

        assert "2020/000001" in result
        assert "2021/000002" in result
        assert result["2020/000001"].name == "2020_000001.html"

    def test_raises_when_no_html_files(self, tmp_path):

        with patch(
            "data_pipeline.extractor.responses.extractor.collect.FilePatterns.FILENAME_REGEX",
            FILENAME_REGEX,
        ):

            with pytest.raises(FileNotFoundError, match="No HTML response files found"):
                collect_html_files(tmp_path)

    def test_raises_when_directory_has_only_empty_subdirs(self, tmp_path):

        (tmp_path / "2020").mkdir()
        with patch(
            "data_pipeline.extractor.responses.extractor.collect.FilePatterns.FILENAME_REGEX",
            FILENAME_REGEX,
        ):

            with pytest.raises(FileNotFoundError):
                collect_html_files(tmp_path)


class TestScanHtmlFiles:
    def test_skips_unrecognised_filenames(self, tmp_path):

        _create_html_file(tmp_path, "2020", "invalid_name.html")
        _create_html_file(tmp_path, "2020", "2020_000001.html")

        with patch(
            "data_pipeline.extractor.responses.extractor.collect.FilePatterns.FILENAME_REGEX",
            FILENAME_REGEX,
        ):

            result = _scan_html_files(tmp_path)

        assert len(result) == 1
        assert "2020/000001" in result

    def test_returns_empty_dict_for_no_files(self, tmp_path):

        with patch(
            "data_pipeline.extractor.responses.extractor.collect.FilePatterns.FILENAME_REGEX",
            FILENAME_REGEX,
        ):

            result = _scan_html_files(tmp_path)

        assert result == {}

    def test_multiple_years(self, tmp_path):

        for year in ["2019", "2020", "2021"]:
            _create_html_file(tmp_path, year, f"{year}_000001.html")

        with patch(
            "data_pipeline.extractor.responses.extractor.collect.FilePatterns.FILENAME_REGEX",
            FILENAME_REGEX,
        ):

            result = _scan_html_files(tmp_path)

        assert len(result) == 3
