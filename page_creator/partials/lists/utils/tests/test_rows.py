"""Tests for build_initiative_row, build_sig_threshold_row, and related helpers."""

import pandas as pd
import pytest
from page_creator.partials.lists.utils.rows import (
    build_initiative_row,
    build_sig_threshold_row,
    build_sig_threshold_rows,
    HEADERS_WITH_SIGNATURES,
)


@pytest.fixture
def base_row():
    return pd.Series(
        {
            "title": "Stop Plastic Pollution",
            "url": "https://eci.ec.europa.eu/001",
            "registration_date": "1 Jan 2020",
            "objective": "Reduce single-use plastic across the EU.",
            "signatures_collected": 1_200_000,
            "signatures_threshold_met": 9,
        }
    )


class TestBuildInitiativeRow:
    def test_contains_title(self, base_row):

        result = build_initiative_row(base_row)
        assert "Stop Plastic Pollution" in result

    def test_contains_url_as_href(self, base_row):

        result = build_initiative_row(base_row)
        assert 'href="https://eci.ec.europa.eu/001"' in result

    def test_contains_registration_date(self, base_row):

        result = build_initiative_row(base_row)
        assert "1 Jan 2020" in result

    def test_contains_truncated_objective(self, base_row):

        result = build_initiative_row(base_row)
        assert "Reduce single-use plastic" in result

    def test_opens_in_new_tab(self, base_row):

        result = build_initiative_row(base_row)
        assert 'target="_blank"' in result

    def test_extra_cells_appended(self, base_row):

        result = build_initiative_row(base_row, extra_cells="<td>EXTRA</td>")
        assert "<td>EXTRA</td>" in result

    def test_missing_url_falls_back_to_hash(self, base_row):

        row = base_row.copy()
        row["url"] = None
        result = build_initiative_row(row)
        assert 'href="#"' in result

    def test_wrapped_in_tr(self, base_row):

        result = build_initiative_row(base_row)
        assert result.strip().startswith("<tr>") or "<tr>" in result
        assert "</tr>" in result


class TestBuildSigThresholdRow:
    def test_contains_signature_count(self, base_row):

        result = build_sig_threshold_row(base_row)
        assert "1,200,000" in result

    def test_contains_threshold_fraction(self, base_row):

        result = build_sig_threshold_row(base_row)
        assert "9 /" in result

    def test_contains_progress_bar(self, base_row):

        result = build_sig_threshold_row(base_row)
        assert "progress-bar" in result

    def test_null_signatures_shows_collection_not_started(self, base_row):

        row = base_row.copy()
        row["signatures_collected"] = None
        row["signatures_threshold_met"] = None
        result = build_sig_threshold_row(row)
        assert "Collection not started" in result


class TestBuildSigThresholdRows:
    def test_concatenates_all_rows(self, base_row):

        df = pd.DataFrame([base_row, base_row])
        result = build_sig_threshold_rows(df)
        assert result.count("Stop Plastic Pollution") == 2

    def test_empty_df_returns_empty_string(self):

        df = pd.DataFrame(
            columns=[
                "title",
                "url",
                "registration_date",
                "objective",
                "signatures_collected",
                "signatures_threshold_met",
            ]
        )
        assert build_sig_threshold_rows(df) == ""


class TestHeadersWithSignatures:
    def test_has_five_columns(self):

        assert len(HEADERS_WITH_SIGNATURES) == 5

    def test_contains_expected_headers(self):

        assert "Initiative" in HEADERS_WITH_SIGNATURES
        assert "Registration" in HEADERS_WITH_SIGNATURES
        assert "Signatures" in HEADERS_WITH_SIGNATURES
        assert "Countries Threshold" in HEADERS_WITH_SIGNATURES
