"""
commission_answer_text
----------------------
Convert the raw ``commission_answer_text`` cell loaded from
``eci_responses_*.csv`` (a stringified Python list of paragraph strings)
into the single, narrative paragraph used in the dashboard CSV.

The reference output (``initiatives_*.csv``) shows one concise paragraph per
initiative, not a verbatim concatenation of the raw paragraphs,
that reduces multi-paragraph Commission answers to a
single readable sentence/paragraph.
"""

import ast
import logging

logger = logging.getLogger(__name__)


def _summarise(paragraphs: list[str]) -> str:
    """Summarise the parsed paragraphs into a single narrative paragraph.

    Note:
        This currently implements a basic concatenation and boilerplate filter.
    """
    cleaned_paragraphs = []

    for p in paragraphs:
        if not isinstance(p, str):
            continue

        cleaned = p.strip()

        # Skip empty paragraphs and known useless boilerplate
        if not cleaned:
            continue

        cleaned_paragraphs.append(cleaned)

    return "\n".join(cleaned_paragraphs)


def extract(raw_cell: str | None) -> str:
    """Return the dashboard-ready commission answer text.

    Args:
        raw_cell: Raw value of the ``commission_answer_text`` column for an
                  initiative, or ``None`` / empty string when the Commission
                  has not yet answered the initiative.

    Returns:
        Single-paragraph narrative summary, or an empty string when the
        initiative has no Commission answer.
    """

    # 1. Handle None / empty
    if not raw_cell or not str(raw_cell).strip():
        return ""

    # 2. Parse the Python list literal with ast.literal_eval
    try:
        parsed_paragraphs = ast.literal_eval(raw_cell)

    except (ValueError, SyntaxError) as exc:
        logger.warning(
            "Failed to parse commission_answer_text literal. Returning empty string. Error: %s",
            exc,
        )
        return ""

    if not isinstance(parsed_paragraphs, list):
        logger.warning(
            "Expected commission_answer_text to parse into a list, got %s",
            type(parsed_paragraphs).__name__,
        )
        return ""

    # 3. Summarise the parsed paragraphs into a single narrative paragraph
    return _summarise(parsed_paragraphs)
