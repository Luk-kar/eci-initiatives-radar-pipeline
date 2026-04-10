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

PATTERNS: list[re.Pattern] = [
    # "did not / does not / will not adopt / propose / introduce / submit"
    re.compile(
        r"\b(?:did\s+not|does\s+not|will\s+not|not\s+intend(?:s|ed)?(?:\s+to)?)"
        r"\s+(?:adopt|propose|introduce|submit|bring\s+forward)\b",
        re.IGNORECASE,
    ),
    # "rejected the proposal / initiative / request"
    re.compile(
        r"\b(?:reject(?:ed|s|ing)?|refus(?:ed|es|ing)?)\s+(?:the\s+)?"
        r"(?:proposal|initiative|request|petition)\b",
        re.IGNORECASE,
    ),
    # "decided not to repeal" / "no intention to repeal" / "will not repeal"
    re.compile(
        r"\b(?:decided?\s+not\s+to\s+repeal"
        r"|no\s+intention\s+to\s+repeal"
        r"|will\s+not\s+repeal"
        r"|not\s+(?:going\s+to\s+)?repeal)\b",
        re.IGNORECASE,
    ),
    # "withdrawn" / "withdrew" / "withdrawal of"
    re.compile(
        r"\b(?:withdraw[ns]?|withdrew|withdrawal\s+of)\b",
        re.IGNORECASE,
    ),
    # "outside (the) (EU) competence" / "falls outside" / "beyond competence"
    re.compile(
        r"\b(?:outside\s+(?:the\s+)?(?:EU\s+)?competence"
        r"|falls?\s+outside"
        r"|beyond\s+(?:the\s+)?competence"
        r"|no\s+(?:EU\s+)?competence)\b",
        re.IGNORECASE,
    ),
    # "will not make / bring forward a legislative proposal"
    re.compile(
        r"\bwill\s+not\s+(?:make|bring\s+forward|introduce)\s+a\s+legislative\s+proposal\b",
        re.IGNORECASE,
    ),
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
        if not item.strip():
            continue
        for pattern in PATTERNS:
            if pattern.search(item):
                logger.debug("REJECTED_LEGISLATION hit in: %.80s", item)
                return True
    return False
