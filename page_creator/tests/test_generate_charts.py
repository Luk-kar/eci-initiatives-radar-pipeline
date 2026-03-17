"""Tests for _find_latest_csv, _fn_to_key, _discover_slot_map, and _build_generated_js."""

import re
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from page_creator.generate_charts import (
    _PATTERN,
    _PREFIX_MAP,
    _build_generated_js,
    _find_latest_csv,
    _fn_to_key,
)


# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_csv(path: Path, content: str = "col\nval\n") -> Path:
    path.write_text(content, encoding="utf-8")
    return path


# ── _find_latest_csv ──────────────────────────────────────────────────────────


class TestFindLatestCsv:

    def test_returns_path_and_date(self, tmp_path):
        _make_csv(tmp_path / "initiatives_2025-06-01_10-00-00.csv")
        path, date = _find_latest_csv(tmp_path)
        assert isinstance(path, Path)
        assert date == "2025-06-01"

    def test_returns_most_recent_by_timestamp(self, tmp_path):
        _make_csv(tmp_path / "initiatives_2024-01-01_08-00-00.csv")
        _make_csv(tmp_path / "initiatives_2025-06-15_12-30-00.csv")
        _make_csv(tmp_path / "initiatives_2023-12-31_23-59-59.csv")
        _, date = _find_latest_csv(tmp_path)
        assert date == "2025-06-15"

    def test_skips_files_without_valid_timestamp(self, tmp_path):
        _make_csv(tmp_path / "initiatives_backup.csv")
        _make_csv(tmp_path / "initiatives_2025-03-10_09-00-00.csv")
        _, date = _find_latest_csv(tmp_path)
        assert date == "2025-03-10"

    def test_raises_if_data_dir_missing(self, tmp_path):
        missing = tmp_path / "nonexistent"
        with pytest.raises(FileNotFoundError, match="Data directory not found"):
            _find_latest_csv(missing)

    def test_raises_if_no_csv_files(self, tmp_path):
        with pytest.raises(
            FileNotFoundError, match="No 'initiatives_\\*.csv' files found"
        ):
            _find_latest_csv(tmp_path)

    def test_raises_if_only_malformed_timestamps(self, tmp_path):
        _make_csv(tmp_path / "initiatives_backup.csv")
        _make_csv(tmp_path / "initiatives_bad-date.csv")
        with pytest.raises(ValueError, match="valid timestamp"):
            _find_latest_csv(tmp_path)

    def test_raises_on_corrupted_csv(self, tmp_path):
        bad = tmp_path / "initiatives_2025-05-01_10-00-00.csv"
        bad.write_bytes(b"\x00\xff\xfe" * 100)  # binary garbage
        with pytest.raises(ValueError, match="corrupted"):
            _find_latest_csv(tmp_path)

    def test_raises_on_newest_corrupted_with_no_fallback(self, tmp_path):
        bad = tmp_path / "initiatives_2026-01-01_00-00-00.csv"
        bad.write_bytes(b"\x00\xff\xfe" * 100)
        _make_csv(tmp_path / "initiatives_2025-06-01_10-00-00.csv")
        with pytest.raises(ValueError, match="corrupted"):
            _find_latest_csv(tmp_path)

    def test_returned_path_exists(self, tmp_path):
        _make_csv(tmp_path / "initiatives_2025-09-20_14-00-00.csv")
        path, _ = _find_latest_csv(tmp_path)
        assert path.exists()

    def test_date_format_is_yyyy_mm_dd(self, tmp_path):
        _make_csv(tmp_path / "initiatives_2024-11-30_08-45-00.csv")
        _, date = _find_latest_csv(tmp_path)
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", date)


# ── _fn_to_key ────────────────────────────────────────────────────────────────


class TestFnToKey:

    def _mock_fn(self, name: str, module: str) -> MagicMock:
        fn = MagicMock()
        fn.__name__ = name
        fn.__module__ = module
        return fn

    def test_chart_function(self):
        fn = self._mock_fn(
            "generate_chart_outcomes", "page_creator.partials.charts.outcomes"
        )
        assert _fn_to_key(fn) == "chart_outcomes.html"

    def test_list_function(self):
        fn = self._mock_fn(
            "generate_collection_ongoing",
            "page_creator.partials.lists.collection_ongoing",
        )
        assert _fn_to_key(fn) == "list_collection_ongoing.html"

    def test_counter_function_no_prefix(self):
        fn = self._mock_fn("generate_kpi_row", "page_creator.partials.counters.kpi_row")
        assert _fn_to_key(fn) == "kpi_row.html"

    def test_date_stamp_function_no_prefix(self):
        fn = self._mock_fn(
            "generate_last_data_update",
            "page_creator.partials.date_stamp.last_data_update",
        )
        assert _fn_to_key(fn) == "last_data_update.html"

    def test_raises_on_unknown_subdir(self):
        fn = self._mock_fn(
            "generate_something", "page_creator.partials.unknown.something"
        )
        with pytest.raises(ValueError, match="not registered in _PREFIX_MAP"):
            _fn_to_key(fn)

    def test_raises_on_wrong_naming_pattern(self):
        fn = self._mock_fn("build_kpi_row", "page_creator.partials.counters.kpi_row")
        with pytest.raises(ValueError, match="naming pattern"):
            _fn_to_key(fn)

    def test_chart_prefix_not_duplicated(self):
        fn = self._mock_fn(
            "generate_chart_ecis_year", "page_creator.partials.charts.ecis_year"
        )
        result = _fn_to_key(fn)
        assert result == "chart_ecis_year.html"
        assert "chart_chart" not in result

    def test_list_prefix_not_duplicated(self):
        fn = self._mock_fn(
            "generate_law_passed", "page_creator.partials.lists.law_passed"
        )
        result = _fn_to_key(fn)
        assert result == "list_law_passed.html"
        assert "list_list" not in result


# ── _build_generated_js ───────────────────────────────────────────────────────


class TestBuildGeneratedJs:

    def test_returns_string(self):
        result = _build_generated_js({"chart_outcomes.html": "chart-outcomes-slot"})
        assert isinstance(result, str)

    def test_contains_auto_generated_comment(self):
        result = _build_generated_js({})
        assert (
            "// AUTO-GENERATED by page_creator/generate_charts.py — do not edit manually."
            in result
        )

    def test_contains_const_declaration(self):
        result = _build_generated_js({})
        assert "const GENERATED_PARTIALS = [" in result

    def test_contains_filename_entry(self):
        result = _build_generated_js({"chart_outcomes.html": "chart-outcomes-slot"})
        assert '["partials/chart_outcomes.html", "chart-outcomes-slot"],' in result

    def test_contains_slot_id_entry(self):
        result = _build_generated_js({"chart_outcomes.html": "chart-outcomes-slot"})
        assert '"chart-outcomes-slot"' in result
        assert 'id="chart-outcomes-slot"' not in result

    def test_multiple_entries_all_present(self):
        slot_map = {
            "chart_outcomes.html": "chart-outcomes-slot",
            "list_law_passed.html": "list-law-passed-slot",
            "kpi_row.html": "kpi-row-slot",
        }
        result = _build_generated_js(slot_map)
        for filename, slot_id in slot_map.items():
            assert f'["partials/{filename}", "{slot_id}"],' in result

    def test_empty_slot_map_produces_empty_array(self):
        result = _build_generated_js({})
        assert "const GENERATED_PARTIALS = [\n\n];" in result

    def test_entries_are_arrays_of_two_strings(self):
        result = _build_generated_js({"kpi_row.html": "kpi-row-slot"})
        assert '["partials/kpi_row.html", "kpi-row-slot"],' in result
