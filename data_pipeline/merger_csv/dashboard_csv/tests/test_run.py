"""Tests for data_pipeline.merger_csv.dashboard_csv.run."""

from pathlib import Path
from unittest.mock import Mock, patch

from data_pipeline.merger_csv.dashboard_csv.run import _sort_results_by_initiative, run


class TestSortResultsByInitiative:
    """Tests for the _sort_results_by_initiative helper."""

    def test_sorts_by_year_date_title(self):
        """It should sort DashboardRows by year, then date, then title."""
        row1 = Mock(registration_year="2024", registration_date="01/01/2024", title="C")
        row2 = Mock(registration_year="2024", registration_date="01/01/2024", title="A")
        row3 = Mock(registration_year="2023", registration_date="15/12/2023", title="B")

        results = [row1, row2, row3]

        sorted_results = _sort_results_by_initiative(results)

        # 2023 comes first
        assert sorted_results[0] == row3
        # 2024, tie-break on title 'A'
        assert sorted_results[1] == row2
        # 2024, tie-break on title 'C'
        assert sorted_results[2] == row1


class TestRun:
    """Tests for the main run() coordinator function."""

    @patch("data_pipeline.merger_csv.dashboard_csv.run.write_output")
    @patch("data_pipeline.merger_csv.dashboard_csv.run.assemble_results")
    @patch("data_pipeline.merger_csv.dashboard_csv.run.sort_by_registration_number")
    @patch("data_pipeline.merger_csv.dashboard_csv.run.collect_source_rows")
    @patch("data_pipeline.merger_csv.dashboard_csv.run.setup")
    def test_run_orchestrates_pipeline(
        self,
        mock_setup,
        mock_collect,
        mock_sort,
        mock_assemble,
        mock_write,
    ):
        """It should coordinate setup, collection, sorting, assembly, and writing."""

        # Arrange
        mock_data_dir = Path("/fake/data")
        mock_logger = Mock()
        mock_setup.return_value = (mock_data_dir, mock_logger)

        mock_init_row = Mock()
        mock_sorted_init = Mock()
        mock_responses = {"1": Mock()}
        mock_legislation = {"1": Mock()}

        mock_collect.return_value = ([mock_init_row], mock_responses, mock_legislation)
        mock_sort.return_value = [mock_sorted_init]

        mock_dashboard_row = Mock()
        mock_assemble.return_value = [mock_dashboard_row]

        expected_output_path = Path("/fake/data/dashboard.csv")
        mock_write.return_value = expected_output_path

        # Act
        result_path = run()

        # Assert
        assert result_path == expected_output_path

        mock_setup.assert_called_once()
        mock_collect.assert_called_once_with(mock_data_dir)
        mock_sort.assert_called_once_with([mock_init_row])
        mock_assemble.assert_called_once_with(
            [mock_sorted_init], mock_responses, mock_legislation
        )
        mock_write.assert_called_once_with(mock_data_dir, [mock_dashboard_row])
