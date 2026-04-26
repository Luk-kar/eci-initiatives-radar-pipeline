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
    """Parse a CSV cell that stores a Python list literal of strings.

    Args:
        raw: Raw cell value.
        column: Source column name for error messages.

    Returns:
        Parsed list of non-empty strings.

    Raises:
        ValueError: If the value is missing, malformed, or not a list.
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


def parse_optional_text_list(raw: str | None, column: str) -> list[str]:
    """Parse an optional list-literal cell.

    Missing values and blank strings are treated as no items. This is used for
    optional follow-up columns because some runs store follow-up text directly in
    eci_responses.csv while others store it only in eci_responses_followup.csv.
    """
    if raw is None:
        return []

    if not str(raw).strip():
        return []

    return parse_text_list(raw, column)


def merge_deduplicated_text_lists(*groups: list[str]) -> list[str]:
    """Merge text groups while preserving order and removing exact duplicates."""
    merged: list[str] = []
    seen: set[str] = set()

    for group in groups:
        for item in group:
            if item in seen:
                continue
            seen.add(item)
            merged.append(item)

    return merged


def split_text_lists(
    responses_row: dict[str, str],
    followup_row: dict[str, str] | None,
) -> tuple[list[str], list[str]]:
    """
    Parse and split source text into (commission_answer_items, followup_items).

    - commission_answer_items → parsed list literal from
      ``eci_responses.commission_answer_text``
    - followup_items → parsed list literal from
      ``eci_responses.followup_events`` (when embedded) merged with
      ``eci_responses_followup.followup_events`` (when present),
      deduplicated while preserving first-seen order

    Raises:
        ValueError: missing/malformed commission_answer_text or
                    malformed follow-up list literal.
    """
    answer_items = parse_text_list(
        responses_row.get("commission_answer_text"),
        "commission_answer_text",
    )

    embedded_followup_items = parse_optional_text_list(
        responses_row.get("followup_events"),
        "followup_events",
    )

    followup_items: list[str] = []
    if followup_row is not None:
        followup_items = parse_optional_text_list(
            followup_row.get("followup_events"),
            "followup_events",
        )

    merged_followup = merge_deduplicated_text_lists(
        embedded_followup_items, followup_items
    )
    return answer_items, merged_followup


def concatenate_text_lists(
    responses_row: dict[str, str],
    followup_row: dict[str, str] | None,
) -> list[str]:
    """Backwards-compatible wrapper — returns answers ⊕ follow-ups, deduplicated."""

    answer_items, followup_items = split_text_lists(responses_row, followup_row)

    return merge_deduplicated_text_lists(answer_items, followup_items)


def assemble_results(
    responses_rows: list[dict[str, str]],
    followup_rows: list[dict[str, str]],
) -> list[LegislationResult]:
    """Join responses with follow-up data and analyse each initiative.

    Args:
        responses_rows: Source responses rows.
        followup_rows: Source follow-up rows.

    Returns:
        Extracted LegislationResult rows.
    """
    followup_index = index_by_registration(followup_rows) if followup_rows else {}

    results: list[LegislationResult] = []
    total = len(responses_rows)

    for i, response_row in enumerate(responses_rows, start=1):

        regnum = response_row.get("registration_number", "").strip()

        if not regnum:
            raise ValueError(
                f"Responses row {i} has an empty registration_number. "
                f"Source CSV is malformed. Row={str(response_row)[:120]}"
            )

        logger.info("Analysing legislation follow-up for %s (%d/%d)", regnum, i, total)

        followup_row = followup_index.get(regnum)

        answer_items, followup_items = split_text_lists(response_row, followup_row)
        text_items = merge_deduplicated_text_lists(answer_items, followup_items)

        logger.info(
            "Prepared %d answer item(s) and %d follow-up item(s) for %s",
            len(answer_items),
            len(followup_items),
            regnum,
        )

        result = analyse_row(
            regnum,
            text_items=text_items,
            commission_answer_items=answer_items,
            followup_items=followup_items,
        )
        results.append(result)

    logger.info("Assembled %d legislation result rows", len(results))
    return results
