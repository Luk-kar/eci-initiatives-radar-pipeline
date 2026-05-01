from dataclasses import fields as dataclass_fields

from data_pipeline.merger_csv.responses_followup_legislation import session
from data_pipeline.merger_csv.responses_followup_legislation.extractor import (
    LegislationResult,
)


class TestSessionConstants:
    def test_output_fieldnames_match_legislation_result_fields(self):

        expected = [field.name for field in dataclass_fields(LegislationResult)]

        assert session.OUTPUT_FIELDNAMES == expected

    def test_responses_glob_targets_responses_csv_files(self):

        assert session.RESPONSES_GLOB == "eci_responses_[0-9]*.csv"

    def test_followup_glob_targets_followup_csv_files(self):

        assert session.FOLLOWUP_GLOB == "eci_responses_followup_[0-9]*.csv"

    def test_responses_cols_define_required_response_columns(self):

        assert session.RESPONSES_COLS == (
            "registration_number",
            "commission_answer",
        )

    def test_followup_cols_define_required_followup_columns(self):

        assert session.FOLLOWUP_COLS == (
            "registration_number",
            "followup_events",
        )
