# law_passed
# -----------
# Convert the raw law_passed cell (loaded from the CSV — a stringified Python
# list of paragraph strings) into a list of plain-text strings with markdown
# links flattened.

import ast
import logging
import re

logger = logging.getLogger(__name__)

# Matches markdown links: [Link Text](url)
MDLINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def flatten_markdown_links(text: str) -> str:
    """Replace markdown links with just their anchor text."""
    return MDLINK_RE.sub(r"\1", text)


def extract(law_passed_raw: str | None) -> list[str]:
    """
    Return the dashboard legislation entries as a list of plain-text strings.

    Args:
        law_passed_raw: Raw value of the law_passed column — a Python list
                        literal, or empty/None.

    Returns:
        List of plain-text legislation strings (may be empty).

    Raises:
        ValueError: If the raw string cannot be parsed as a Python literal.
        TypeError:  If the parsed literal is not a list.
    """

    # 1. Early-return when empty
    if not law_passed_raw or not str(law_passed_raw).strip():
        return None

    # 2. Parse law_passed_raw as a Python list literal
    try:
        parsed_paragraphs = ast.literal_eval(law_passed_raw)

    except (ValueError, SyntaxError) as exc:
        raise ValueError(
            f"Failed to parse law_passed literal {law_passed_raw!r}"
        ) from exc

    if not isinstance(parsed_paragraphs, list):
        raise TypeError(
            f"Expected law_passed to parse into a list, "
            f"got {type(parsed_paragraphs).__name__}"
        )

    # 3. Flatten Markdown links, strip, and filter
    result = []

    for p in parsed_paragraphs:

        if not isinstance(p, str):
            continue

        cleaned = flatten_markdown_links(p.strip())

        if cleaned:
            result.append(cleaned)

    return result if result else None
