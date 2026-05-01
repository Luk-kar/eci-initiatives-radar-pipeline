import ast
import logging
import re

from .utils._regex import normalize_newlines

logger = logging.getLogger(__name__)


def _summarise_paragraphs(paragraphs: list[str]) -> str:
    """Summarise the parsed paragraphs into a single narrative paragraph.

    Note: This currently implements a basic concatenation and boilerplate filter.
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

    joined_text = "\n".join(cleaned_paragraphs)

    # Use the shared utility to collapse any multi-newlines
    return normalize_newlines(joined_text)


def extract(raw_cell: str | None) -> str:
    """Return the dashboard-ready commission answer text."""
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
            "Expected commission_answer_text to parse into a list, got: %s",
            type(parsed_paragraphs).__name__,
        )
        return ""

    # 3. Summarise the parsed paragraphs into a single narrative paragraph
    return _summarise_paragraphs(parsed_paragraphs)
