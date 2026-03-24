"""
Tests for data_pipeline.extractor.initiatives.extractor.
"""

import csv
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from data_pipeline.extractor.extractor_shared.errors import HTMLParseError
from data_pipeline.extractor.initiatives.extractor import extract_initiatives
from data_pipeline.extractor.initiatives.model import ECIInitiativeDetailsRecord

from data_pipeline.pipeline_shared.consts import FILE_ENCODING

_PARSER_PARSE = "data_pipeline.extractor.initiatives.parser.ECIHTMLParser.parse"

# ── Helpers ────────────────────────────────────────────────────────────────────


def _make_year_dir(base: Path, year: str = "2023") -> Path:
    year_dir = base / year
    year_dir.mkdir(parents=True)
    return year_dir


def _write_html(year_dir: Path, name: str, content: str = "<html></html>") -> Path:
    html_file = year_dir / name
    html_file.write_text(content, encoding=FILE_ENCODING)
    return html_file


def _minimal_record() -> dict:
    return {name: "" for name in ECIInitiativeDetailsRecord.model_fields}


# ── extract_initiatives ────────────────────────────────────────────────────────


class TestExtractInitiatives:

    def test_raises_when_source_dir_missing(self, tmp_path):

        source_dir = tmp_path / "nonexistent"
        output_csv = tmp_path / "out.csv"

        with pytest.raises(FileNotFoundError, match="No HTML files found"):
            extract_initiatives(source_dir, output_csv)

    def test_raises_when_no_html_files(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        _make_year_dir(source_dir)
        output_csv = tmp_path / "out.csv"

        with pytest.raises(FileNotFoundError, match="No HTML files found"):
            extract_initiatives(source_dir, output_csv)

    def test_raises_when_all_html_files_are_empty(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html", content="")
        output_csv = tmp_path / "out.csv"

        with pytest.raises(FileNotFoundError, match="No HTML files found"):
            extract_initiatives(source_dir, output_csv)

    def test_creates_output_csv_with_correct_headers(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html")
        output_csv = tmp_path / "out.csv"

        expected_columns = [name for name in ECIInitiativeDetailsRecord.model_fields]

        with patch(
            _PARSER_PARSE,
            return_value=_minimal_record(),
        ):
            extract_initiatives(source_dir, output_csv)

        assert output_csv.exists()
        with open(output_csv, encoding=FILE_ENCODING) as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames == expected_columns

    def test_writes_one_row_per_html_file(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html")
        _write_html(year_dir, "2023_000002.html")

        output_csv = tmp_path / "out.csv"

        with patch(
            _PARSER_PARSE,
            return_value=_minimal_record(),
        ):
            extract_initiatives(source_dir, output_csv)

        with open(output_csv, encoding=FILE_ENCODING) as f:
            rows = list(csv.DictReader(f))

        assert len(rows) == 2

    def test_creates_output_parent_dirs(self, tmp_path):
        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html")
        output_csv = tmp_path / "nested" / "deep" / "out.csv"

        with patch(
            _PARSER_PARSE,
            return_value=_minimal_record(),
        ):
            extract_initiatives(source_dir, output_csv)

        assert output_csv.exists()

    def test_raises_html_parse_error_on_parse_failure(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html")
        output_csv = tmp_path / "out.csv"

        with patch(
            _PARSER_PARSE,
            side_effect=ValueError("bad HTML"),
        ):
            with pytest.raises(HTMLParseError, match="Failed to parse"):
                extract_initiatives(source_dir, output_csv)

    def test_ignores_non_year_directories(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        source_dir.mkdir()
        (source_dir / "misc").mkdir()

        _write_html(source_dir / "misc", "misc.html")
        output_csv = tmp_path / "out.csv"

        with pytest.raises(FileNotFoundError):
            extract_initiatives(source_dir, output_csv)

    def test_processes_multiple_years(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        _write_html(_make_year_dir(source_dir, "2022"), "2022_000001.html")
        _write_html(_make_year_dir(source_dir, "2023"), "2023_000001.html")

        output_csv = tmp_path / "out.csv"

        with patch(
            _PARSER_PARSE,
            return_value=_minimal_record(),
        ):
            extract_initiatives(source_dir, output_csv)

        with open(output_csv, encoding=FILE_ENCODING) as f:
            rows = list(csv.DictReader(f))

        assert len(rows) == 2

    def test_missing_fields_default_to_empty_string(self, tmp_path):

        source_dir = tmp_path / "initiatives"
        year_dir = _make_year_dir(source_dir)

        _write_html(year_dir, "2023_000001.html")
        output_csv = tmp_path / "out.csv"

        with patch(
            _PARSER_PARSE,
            return_value={"registration_number": "ECI(2023)000001"},
        ):
            extract_initiatives(source_dir, output_csv)

        with open(output_csv, encoding=FILE_ENCODING) as f:
            row = list(csv.DictReader(f))[0]

        assert row["title"] == ""
        assert row["registration_number"] == "ECI(2023)000001"
