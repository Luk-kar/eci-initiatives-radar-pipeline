"""
rejected_legislation.py
-----------------------
Regex patterns and extractor for the ``Rejected_Legislation`` output column.

``extract(text_items)`` returns ``True`` as soon as any REJECTED_LEGISLATION
pattern fires across the combined text items for an initiative.
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

# ── Patterns (compiled once at module load) ───────────────────────────────────

_MARKDOWN_LINK_REGEX: re.Pattern = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def _normalise(text: str) -> str:
    """
    Strip Markdown hyperlinks, keeping only the visible label text.

    Example:
        ``[Sustainable Use Directive](https://ec.europa.eu/...)``
        → ``Sustainable Use Directive``

    Args:
        text: Raw text fragment from the source CSV.

    Returns:
        Text with all ``[label](url)`` constructs replaced by ``label``.
    """
    return _MARKDOWN_LINK_REGEX.sub(r"\1", text)


REJECTION_REASONING_KEYWORDS = [
    r"will not make\s.+legisla[a-z]",
    r"will not propose",
    r"no legislative proposal",
    r"no new legislation",
    r"not to submit a legislative proposal",
    r"no repeal of that legislation",
    r"not necessary to propose a new legal",
    r"not to submit\b.+\blegisla[a-z]+\b",
    r"(outside|beyond)\b.+\competence",
    r"not.+propose.+legal",
    r"no further legal acts",
]

PATTERNS: list[re.Pattern] = [
    re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
    for keyword in REJECTION_REASONING_KEYWORDS
]

# ── Extractor ─────────────────────────────────────────────────────────────────


def extract(text_items: list[str]) -> bool:
    """
    Scan *text_items* for REJECTED_LEGISLATION pattern matches.

    Evaluation stops at the first match (short-circuit): a single hit is
    sufficient to set the flag.

    Args:
        text_items: Pre-merged list of text fragments for one initiative.

    Returns:
        ``True`` when at least one pattern fires, ``False`` otherwise.
    """
    for item in text_items:

        normalised = _normalise(item).strip()

        if not item.strip():
            continue

        for pattern in PATTERNS:
            if pattern.search(item):
                logger.debug("REJECTED_LEGISLATION hit in: %.80s", item)
                return True

    return False
