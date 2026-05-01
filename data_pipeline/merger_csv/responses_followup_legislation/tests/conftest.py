from __future__ import annotations

import pytest

from data_pipeline.merger_csv.responses_followup_legislation.extractor import (
    LegislationResult,
)


@pytest.fixture
def responses_rows() -> list[dict[str, str]]:
    return [
        {
            "registration_number": "2012/000001",
            "commission_answer": "['Commission answer 1', 'Commission answer 2']",
        },
        {
            "registration_number": "2012/000002",
            "commission_answer": "['Commission answer 3']",
        },
    ]


@pytest.fixture
def followup_rows() -> list[dict[str, str]]:
    return [
        {
            "registration_number": "2012/000001",
            "followup_events": "['Follow-up 1', 'Follow-up 2']",
        },
        {
            "registration_number": "2012/000002",
            "followup_events": "['Follow-up 3']",
        },
    ]


@pytest.fixture
def legislation_results() -> list[LegislationResult]:
    return [
        LegislationResult(
            registration_number="2012/000001",
            commission_answer=["Commission answer 1", "Commission answer 2"],
            followup_events=["Follow-up 1", "Follow-up 2"],
            law_passed=["Follow-up 1"],
            is_law_passed=True,
            Rejected_Legislation=False,
        ),
        LegislationResult(
            registration_number="2012/000002",
            commission_answer=["Commission answer 3"],
            followup_events=["Follow-up 3"],
            law_passed=None,
            is_law_passed=False,
            Rejected_Legislation=True,
        ),
    ]
