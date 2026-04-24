"""
Legislation Extraction Assembly
Combines source text and prepares initiative-level inputs for legislation analysis.
"""

import ast
import logging

from .collect import index_by_registration
from .extractor import LegislationResult, analyse_row

logger = logging.getLogger(__name__)


def parse_text_list(raw: str | None, column: str) -> list[str]:
    """
    Parse a CSV cell that stores a Python list literal of strings.

    Args:
        raw:    Raw cell value.
        column: Source column name for error messages.

    Returns:
        Parsed list of non-empty strings.

    Raises:
        ValueError: if the value is missing, malformed, or not a list of strings.
    """

    if raw is None:
        raise ValueError(f"Column {column!r} is missing.")

    try:
        parsed = ast.literal_eval(raw)

    except (ValueError, SyntaxError) as exc:

        raise ValueError(
            f"Column {column!r} is not a valid Python literal: {raw!r}"
        ) from exc

    if parsed is None:
        return []

    if not isinstance(parsed, list):
        raise ValueError(
            f"Column {column!r} expected a list, got {type(parsed).__name__}: {raw!r}"
        )

    items: list[str] = []

    for item in parsed:
        if item is None:
            continue

        text = str(item).strip()
        if text:
            items.append(text)

    return items


def concatenate_text_lists(
    responses_row: dict[str, str],
    followup_row: dict[str, str] | None,
) -> list[str]:
    """
    Combine ``commission_answer_text`` and ``followup_events`` into one list.

    Args:
        responses_row: Row from responses CSV.
        followup_row:  Matching row from follow-up CSV, if present.

    Returns:
        Combined text list.

    Raises:
        ValueError: if ``commission_answer_text`` is missing or malformed.
    """

    answer_items = parse_text_list(
        responses_row.get("commission_answer_text"),
        "commission_answer_text",
    )

    followup_items: list[str] = []

    if followup_row is not None:
        
        followup_items = parse_text_list(
            followup_row.get("followup_events"),
            "followup_events",
        )

    return answer_items + followup_items


def assemble_results(
    responses_rows: list[dict[str, str]],
    followup_rows: list[dict[str, str]],
) -> list[LegislationResult]:
    """
    Join responses with follow-up data and analyse each initiative.

    Args:
        responses_rows: Source responses rows.
        followup_rows:  Source follow-up rows.

    Returns:
        Extracted ``LegislationResult`` rows.
    """

    followup_index = index_by_registration(followup_rows) if followup_rows else {}
    results: list[LegislationResult] = []

    for i, response_row in enumerate(responses_rows):

        reg_num = response_row["registration_number"].strip()

        if not reg_num:
            raise ValueError(
                f"Responses row {i} has an empty registration_number. "
                f"Source CSV is malformed. Row={str(response_row)[:120]}"
            )

        followup_row = followup_index.get(reg_num)
        text_items = concatenate_text_lists(response_row, followup_row)
        result = analyse_row(reg_num, text_items)
        results.append(result)

    logger.info("Assembled %d legislation result row(s)", len(results))
    return results