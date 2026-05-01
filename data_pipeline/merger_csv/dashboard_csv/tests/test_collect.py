"""Tests for data_pipeline.merger_csv.dashboard_csv.collect."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from data_pipeline.merger_csv.dashboard_csv.collect import (
    _index_by_registration,
    _load_initiatives,
    _load_legislation,
    _load_responses,
    collect_source_rows,
)
from data_pipeline.merger_csv.dashboard_csv.input_models import (
    InitiativeRow,
    LegislationRow,
    ResponseRow,
)


@pytest.fixture
def mock_data_dir():
    """Fixture to provide a fake data directory."""
    return Path("/fake/data/dir")


class TestLoaders:
    """Tests for the individual CSV loader helpers."""

    @patch("data_pipeline.merger_csv.dashboard_csv.collect.filter_columns")
    @patch("data_pipeline.merger_csv.dashboard_csv.collect.load_csv")
    @patch("data_pipeline.merger_csv.dashboard_csv.collect.validate_csv_exists")
    @patch("data_pipeline.merger_csv.dashboard_csv.collect.find_latest_csv")
    def test_load_initiatives(
        self,
        mock_find_latest_csv,
        mock_validate_csv_exists,
        mock_load_csv,
        mock_filter_columns,
        mock_data_dir,
    ):
        mock_find_latest_csv.return_value = Path("dummy_initiatives.csv")
        mock_filter_columns.return_value = [
            {
                "registration_number": "2024/000001",
                "title": "Save the Bees",
                "objective": "Objective",
                "current_status": "Collection Ongoing",
                "initiative_url": "https://example.com/en",
                "timeline_registered": "01/01/2024",
                "timeline_collection_start_date": "01/01/2024",
                "timeline_collection_closed": "01/01/2025",
                "funding_total": "100,000",
                "signatures_collected": "1,000,000",
                "signatures_collected_by_country": "{}",
                "signatures_threshold_met": "7",
            }
        ]

        result = _load_initiatives(mock_data_dir)

        assert len(result) == 1
        assert isinstance(result[0], InitiativeRow)
        assert result[0].registration_number == "2024/000001"

        mock_find_latest_csv.assert_called_once()
        mock_validate_csv_exists.assert_called_once_with(Path("dummy_initiatives.csv"))
        mock_load_csv.assert_called_once()
        mock_filter_columns.assert_called_once()

    @patch("data_pipeline.merger_csv.dashboard_csv.collect.filter_columns")
    @patch("data_pipeline.merger_csv.dashboard_csv.collect.load_csv")
    @patch("data_pipeline.merger_csv.dashboard_csv.collect.validate_csv_exists")
    @patch("data_pipeline.merger_csv.dashboard_csv.collect.find_latest_csv")
    def test_load_responses(
        self,
        mock_find_latest_csv,
        mock_validate_csv_exists,
        mock_load_csv,
        mock_filter_columns,
        mock_data_dir,
    ):
        mock_find_latest_csv.return_value = Path("dummy_responses.csv")
        mock_filter_columns.return_value = [
            {"registration_number": "2024/000001", "commission_answer": "Answer"}
        ]

        result = _load_responses(mock_data_dir)

        assert len(result) == 1
        assert isinstance(result[0], ResponseRow)
        assert result[0].registration_number == "2024/000001"

    @patch("data_pipeline.merger_csv.dashboard_csv.collect.filter_columns")
    @patch("data_pipeline.merger_csv.dashboard_csv.collect.load_csv")
    @patch("data_pipeline.merger_csv.dashboard_csv.collect.validate_csv_exists")
    @patch("data_pipeline.merger_csv.dashboard_csv.collect.find_latest_csv")
    def test_load_legislation(
        self,
        mock_find_latest_csv,
        mock_validate_csv_exists,
        mock_load_csv,
        mock_filter_columns,
        mock_data_dir,
    ):
        mock_find_latest_csv.return_value = Path("dummy_legislation.csv")
        mock_filter_columns.return_value = [
            {
                "registration_number": "2024/000001",
                "followup_events": "Events",
                "Law_Passed": "Yes",
                "Is_Law_Passed": "True",
                "Rejected_Legislation": "False",
            }
        ]

        result = _load_legislation(mock_data_dir)

        assert len(result) == 1
        assert isinstance(result[0], LegislationRow)
        assert result[0].registration_number == "2024/000001"


class TestIndexByRegistration:
    """Tests for the _index_by_registration helper function."""

    def test_index_success(self):
        row1 = Mock(registration_number="2024/000001")
        row2 = Mock(registration_number="2024/000002")

        result = _index_by_registration([row1, row2], "mock_source")

        assert len(result) == 2
        assert result["2024/000001"] == row1
        assert result["2024/000002"] == row2

    def test_missing_registration_number_raises(self):
        row1 = Mock(registration_number="")

        with pytest.raises(
            ValueError, match="mock_source: row 0 has an empty registration_number."
        ):
            _index_by_registration([row1], "mock_source")

    def test_whitespace_registration_number_raises(self):
        row1 = Mock(registration_number="   ")

        with pytest.raises(
            ValueError, match="mock_source: row 0 has an empty registration_number."
        ):
            _index_by_registration([row1], "mock_source")

    def test_duplicate_registration_number_raises(self):
        row1 = Mock(registration_number="2024/000001")
        row2 = Mock(registration_number="2024/000001")

        with pytest.raises(
            ValueError,
            match="mock_source: duplicate registration_number '2024/000001'.",
        ):
            _index_by_registration([row1, row2], "mock_source")


class TestCollectSourceRows:
    """Tests for the main collect_source_rows coordinator function."""

    @patch("data_pipeline.merger_csv.dashboard_csv.collect._load_legislation")
    @patch("data_pipeline.merger_csv.dashboard_csv.collect._load_responses")
    @patch("data_pipeline.merger_csv.dashboard_csv.collect._load_initiatives")
    def test_collect_source_rows(
        self,
        mock_load_initiatives,
        mock_load_responses,
        mock_load_legislation,
        mock_data_dir,
    ):
        mock_init = Mock(registration_number="2024/000001")
        mock_resp = Mock(registration_number="2024/000001")
        mock_leg = Mock(registration_number="2024/000001")

        mock_load_initiatives.return_value = [mock_init]
        mock_load_responses.return_value = [mock_resp]
        mock_load_legislation.return_value = [mock_leg]

        initiatives, responses_idx, legislation_idx = collect_source_rows(mock_data_dir)

        assert initiatives == [mock_init]
        assert responses_idx == {"2024/000001": mock_resp}
        assert legislation_idx == {"2024/000001": mock_leg}

        mock_load_initiatives.assert_called_once_with(mock_data_dir)
        mock_load_responses.assert_called_once_with(mock_data_dir)
        mock_load_legislation.assert_called_once_with(mock_data_dir)
