"""Tests for data_pipeline.merger_csv.dashboard_csv.write."""

import csv
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from data_pipeline.merger_csv.dashboard_csv.extractor import DashboardRow
from data_pipeline.merger_csv.dashboard_csv.session import OUTPUT_FIELDNAMES
from data_pipeline.merger_csv.dashboard_csv.write import write_output
from data_pipeline.pipeline_shared.consts import (
    ECI_DASHBOARD_CSV_PATTERN,
    FILE_ENCODING,
    TIMESTAMP_FORMAT,
)


@pytest.fixture
def dummy_dashboard_row():
    """Fixture for a basic DashboardRow."""
    return DashboardRow(
        registration_number="2024/000001",
        title="Test Initiative",
        registration_year="2024",
        registration_date="01/01/2024",
        current_status="Collection Ongoing",
        objective="Test Objective",
        commission_answer="",
        initiative_url="https://citizens-initiative.europa.eu/initiatives/details/2024/000001_en",
        signatures_collected_by_country="",
        signatures_countries_threshold_met_count="0",
        signatures_collected="1,000",
        funding_total="10,000",
        timeline_collection_closed="01/01/2025",
        timeline_collection_start="01/01/2024",
        law_passed="",
    )


class TestWriteOutput:
    """Tests for writing the dashboard output CSV."""

    @patch("data_pipeline.merger_csv.dashboard_csv.write.datetime")
    @patch("data_pipeline.merger_csv.dashboard_csv.write.logger")
    def test_write_output_generates_correct_csv(
        self,
        mock_logger,
        mock_datetime,
        tmp_path: Path,
        dummy_dashboard_row: DashboardRow,
    ):
        """It should write the expected CSV file with a timestamped name."""
        # Arrange
        mock_datetime.now.return_value = datetime(2024, 12, 31, 23, 59, 59)

        # Build expected filename exactly as the implementation does
        expected_filename = ECI_DASHBOARD_CSV_PATTERN.format(
            timestamp="2024-12-31_23-59-59"
        )
        expected_path = tmp_path / expected_filename

        # Act
        result_path = write_output(tmp_path, [dummy_dashboard_row])

        # Assert Path
        assert result_path == expected_path
        assert result_path.exists()
        assert result_path.is_file()

        # Assert Logs
        mock_logger.info.assert_any_call("Writing dashboard CSV %s", expected_path)
        mock_logger.info.assert_any_call("Wrote %d row(s) to %s", 1, expected_path)

        # Assert CSV content
        with expected_path.open("r", encoding=FILE_ENCODING, newline="") as fh:
            reader = list(csv.DictReader(fh))

            assert len(reader) == 1

            row = reader[0]
            # Ensure headers match the constant allowlist precisely
            assert list(row.keys()) == OUTPUT_FIELDNAMES

            # Ensure fields serialised via model_dump() correctly
            assert row["registration_number"] == "2024/000001"
            assert row["title"] == "Test Initiative"
            assert row["current_status"] == "Collection Ongoing"
