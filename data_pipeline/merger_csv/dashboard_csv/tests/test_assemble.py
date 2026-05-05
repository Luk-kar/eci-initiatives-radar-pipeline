from unittest.mock import MagicMock, patch
import pytest

from data_pipeline.merger_csv.dashboard_csv.assemble import assemble_results
from data_pipeline.merger_csv.dashboard_csv.input_models import (
    InitiativeRow,
    LegislationRow,
    ResponseRow,
)


@pytest.fixture
def initiative_rows():
    return [
        InitiativeRow(
            registration_number="2024/000001",
            title="Initiative 1",
            objective="Objective 1",
            current_status="Collection Ongoing",
            initiative_url="https://citizens-initiative.europa.eu/initiatives/details/2024/000001_en",
            timeline_registered="01/01/2024",
            timeline_collection_start_date="01/01/2024",
            timeline_collection_closed="01/01/2025",
            funding_total="100,000",
            signatures_collected="1,000,000",
            signatures_collected_by_country="{'Germany': {'signatures': 100000, 'threshold': 70000, 'percentage': 142.85}}",
            signatures_countries_threshold_met_count="1",
        )
    ]


@pytest.fixture
def response_index():
    return {
        "2024/000001": ResponseRow(
            registration_number="2024/000001",
            commission_answer="['Answer paragraph 1']",
        )
    }


@pytest.fixture
def legislation_index():
    return {
        "2024/000001": LegislationRow(
            registration_number="2024/000001",
            followup_events="['Follow-up event 1']",
            law_passed="['Law was passed']",
            is_law_passed="True",
            rejected_legislation="False",
        )
    }


class TestAssembleResults:

    @patch("data_pipeline.merger_csv.dashboard_csv.assemble.analyse_row")
    def test_assemble_results_produces_dashboard_rows(
        self, mock_analyse_row, initiative_rows, response_index, legislation_index
    ):
        mock_analyse_row.return_value = MagicMock(current_status="Collection Ongoing")
        results = assemble_results(initiative_rows, response_index, legislation_index)

        assert len(results) == len(initiative_rows)
        assert mock_analyse_row.call_count == len(initiative_rows)

    def test_assemble_results_raises_value_error_for_empty_registration_number(
        self, response_index, legislation_index
    ):
        initiative_rows_bad = [
            InitiativeRow(
                registration_number="",
                title="Initiative 1",
                objective="Objective 1",
                current_status="Collection Ongoing",
                initiative_url="https://citizens-initiative.europa.eu/initiatives/details/2024/000001_en",
                timeline_registered="01/01/2024",
                timeline_collection_start_date="01/01/2024",
                timeline_collection_closed="01/01/2025",
                funding_total="100,000",
                signatures_collected="1,000,000",
                signatures_collected_by_country="",
                signatures_countries_threshold_met_count="1",
            )
        ]

        with pytest.raises(ValueError, match="empty registration_number"):
            assemble_results(initiative_rows_bad, response_index, legislation_index)

    @patch("data_pipeline.merger_csv.dashboard_csv.assemble.analyse_row")
    def test_assemble_results_handles_missing_response_and_legislation(
        self, mock_analyse_row, initiative_rows
    ):
        mock_analyse_row.return_value = MagicMock(current_status="Collection Ongoing")
        results = assemble_results(initiative_rows, {}, {})

        assert len(results) == len(initiative_rows)
        assert mock_analyse_row.call_count == len(initiative_rows)
