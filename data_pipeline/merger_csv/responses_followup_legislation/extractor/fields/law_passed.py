"""
law_passed.py
-------------
Regex patterns and extractor for the ``Law_Passed`` output column.

``extract(text_items)`` scans each item in the combined text list for evidence
that a piece of EU legislation was adopted, applied, or entered into force and
returns the list of matched spans, or ``None`` when nothing fired.
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

# ── Shared legislative vocabulary ─────────────────────────────────────────────

_LEGISLATIVE_TERMS = (
    r"directive|regulation|decision|legislation|law|act|measure|proposal"
)

# ── Patterns (compiled once at module load) ───────────────────────────────────

PATTERNS: list[re.Pattern] = [
    # "adopted the directive / regulation / …"
    re.compile(
        rf"\badopt(?:ed|s|ing)?\s+(?:\w+\s+){{0,4}}(?:{_LEGISLATIVE_TERMS})\b",
        re.IGNORECASE,
    ),
    # "directive / regulation / … was adopted / has been adopted"
    re.compile(
        rf"\b(?:{_LEGISLATIVE_TERMS})\b[^.{{}}]{{0,80}}\badopt(?:ed|s|ing)?\b",
        re.IGNORECASE,
    ),
    # "entered into force" / "enter into force"
    re.compile(
        r"\bentered?\s+into\s+force\b",
        re.IGNORECASE,
    ),
    # "applies / applied / apply … directive / regulation / …"
    re.compile(
        rf"\bappl(?:y|ies|ied|ying)\b[^.{{}}]{{0,80}}\b(?:{_LEGISLATIVE_TERMS})\b",
        re.IGNORECASE,
    ),
    # "implementing / implemented regulation / directive / …"
    re.compile(
        rf"\bimplementi?n?g?\b[^.{{}}]{{0,40}}\b(?:{_LEGISLATIVE_TERMS})\b",
        re.IGNORECASE,
    ),
]


# ── Extractor ─────────────────────────────────────────────────────────────────


def extract(text_items: list[str]) -> list[str] | None:
    """
    Scan *text_items* for LAW_MENTIONED pattern matches.

    Each item is tested independently; all matched spans across all items are
    collected into a flat list.

    Args:
        text_items: Pre-merged list of text fragments for one initiative.

    Returns:
        ``list[str]`` of matched spans when at least one pattern fires,
        ``None`` otherwise.
    """
    matched_spans: list[str] = []

    for item in text_items:
        if not item.strip():
            continue
        for pattern in PATTERNS:
            match = pattern.search(item)
            if match:
                matched_spans.append(match.group(0))
                logger.debug("LAW_MENTIONED hit: %r", match.group(0))

    return matched_spans if matched_spans else None
