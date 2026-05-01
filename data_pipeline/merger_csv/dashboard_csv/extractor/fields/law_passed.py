"""
law_passed
-----------
Convert the raw ``law_passed`` cell loaded from the CSV
(a stringified Python list of paragraph strings) into a single, plain-text
narrative with markdown links flattened.
"""

import ast
import logging
import re

logger = logging.getLogger(__name__)

# Matches markdown links: [Link Text](URL)
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def _flatten_markdown_links(text: str) -> str:
    """Replace markdown links with just their anchor text."""
    return _MD_LINK_RE.sub(r"\1", text)


def extract(law_passed_raw: str | None) -> str:
    """Return the dashboard ``legislation`` narrative.

    Args:
        law_passed_raw:        Raw value of the ``law_passed`` column
                               (Python list literal, or empty / ``None``).

    Returns:
        Plain-text legislation narrative, or an empty string when input is empty.

    Raises:
        ValueError: If the raw string cannot be parsed as a Python literal.
        TypeError:  If the parsed literal is not a list.
    """

    # 1. Early-return "" when empty
    if not law_passed_raw or not str(law_passed_raw).strip():
        return ""

    # 2. Parse law_passed_raw as a Python list literal
    try:
        parsed_paragraphs = ast.literal_eval(law_passed_raw)

    except (ValueError, SyntaxError) as exc:

        # Raise the error instead of logging a warning
        raise ValueError(
            f"Failed to parse law_passed literal: {law_passed_raw!r}"
        ) from exc

    if not isinstance(parsed_paragraphs, list):

        # Raise the error instead of logging a warning
        raise TypeError(
            f"Expected law_passed to parse into a list, got {type(parsed_paragraphs).__name__}"
        )

    cleaned_paragraphs = []

    for p in parsed_paragraphs:
        if not isinstance(p, str):
            continue

        # 3. Flatten Markdown links
        cleaned = _flatten_markdown_links(p).strip()

        if cleaned:
            cleaned_paragraphs.append(cleaned)

    # 4. Join elements by the `\n`
    return "\n".join(cleaned_paragraphs)
