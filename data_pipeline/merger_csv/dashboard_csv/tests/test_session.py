"""Tests for data_pipeline.merger_csv.dashboard_csv.session."""

import logging
from pathlib import Path
from unittest.mock import Mock, patch

from data_pipeline.merger_csv.dashboard_csv.session import (
    INITIATIVE_COLS,
    INITIATIVES_GLOB,
    LEGISLATION_COLS,
    LEGISLATION_GLOB,
    OUTPUT_FIELDNAMES,
    RESPONSE_COLS,
    RESPONSES_GLOB,
    setup,
)


class TestSessionConstants:
    """Tests to ensure column allow-lists and constants are configured correctly."""

    def test_globs_are_strings(self):
        """It should define glob patterns as strings."""

        assert isinstance(INITIATIVES_GLOB, str)
        assert isinstance(RESPONSES_GLOB, str)
        assert isinstance(LEGISLATION_GLOB, str)

    def test_initiative_cols(self):
        """It should define the expected columns for eci_initiatives."""

        assert "registration_number" in INITIATIVE_COLS
        assert "title" in INITIATIVE_COLS
        assert "objective" in INITIATIVE_COLS

    def test_response_cols(self):
        """It should extract only the registration_number and commission_answer."""

        assert list(RESPONSE_COLS) == ["registration_number", "commission_answer"]

    def test_legislation_cols(self):
        """It should explicitly omit commission_answer from legislation."""

        assert "registration_number" in LEGISLATION_COLS
        assert "commission_answer" not in LEGISLATION_COLS
        assert "is_law_passed" in LEGISLATION_COLS
        assert "rejected_legislation" in LEGISLATION_COLS

    def test_output_fieldnames_matches_model(self):
        """It should derive OUTPUT_FIELDNAMES directly from the DashboardRow model keys."""

        assert isinstance(OUTPUT_FIELDNAMES, list)
        assert "registration_number" in OUTPUT_FIELDNAMES
        assert "current_status" in OUTPUT_FIELDNAMES


class TestSessionSetup:
    """Tests for the session bootstrap setup logic."""

    @patch("data_pipeline.merger_csv.dashboard_csv.session.get_logger")
    @patch("data_pipeline.merger_csv.dashboard_csv.session.find_latest_data_dir")
    def test_setup_returns_data_dir_and_logger(
        self, mock_find_latest_data_dir, mock_get_logger
    ):
        """It should locate the run directory, set up the logger, and return both."""

        # Arrange
        mock_data_dir = Path("/fake/data_pipeline/data/2024-01-01_12-00-00")
        mock_find_latest_data_dir.return_value = mock_data_dir

        mock_logger = Mock(spec=logging.Logger)
        mock_get_logger.return_value = mock_logger

        # Act
        data_dir, logger = setup()

        # Assert
        assert data_dir == mock_data_dir
        assert logger == mock_logger

        # Verify it called find_latest_data_dir with the global DATA_DIR constant
        mock_find_latest_data_dir.assert_called_once()

        # Verify it called get_logger with the right arguments
        mock_get_logger.assert_called_once()
        args, _ = mock_get_logger.call_args

        log_dir_path = args[0]
        assert log_dir_path == mock_data_dir / "logs"  # Assuming LOG_DIR_NAME is 'logs'

        # Verify initial logs were written
        assert mock_logger.info.call_count >= 2
