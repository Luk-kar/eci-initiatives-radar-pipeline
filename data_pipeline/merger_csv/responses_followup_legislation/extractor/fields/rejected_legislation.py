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


# Less safe but more future proof
# ── Legislative term building blocks ─────────────────────────────────────────

# Inflections of the "legislat-" root:
_LEGAL = r"legal(?:\'s)?"  # legal / legal's
# legal / legislate / legislated / legislation / legislative / legislatively / legislator
_LEGISLATIVE_FORMS = r"legis(?:lat(?:ion|ive|or|e|ed|ing))?"

_LEGISLATION_TERMS = [_LEGAL, _LEGISLATIVE_FORMS]

_NEGATION_TERMS = [
    r"no",
    r"not",
    r"cannot",
    r"[a-z]+n\'t",  # isn't, wasn't, weren't, shouldn't, wouldn't, couldn't, mightn't, needn't, oughtn't
    r"outside",
    r"beyond",
    r"lack?s",
    r"exceeds competence",
    r"refused to",
    r"declined to",
    r"rejected",
    r"decided against",
    r"chose not to",
    r"opted not to",
    r"will refrain from",
    r"unnecessary to",
]


# ── Pattern compiler ──────────────────────────────────────────────────────────


def _compile_patterns(terms: list[str]) -> list[re.Pattern]:
    if not terms:
        raise ValueError(f"Empty terms list: {terms!r}")

    patterns = []

    for term in terms:

        if not term:
            raise ValueError(f"Empty term string: {term!r}")

        spaced = re.sub(r" ", r"\\s+", term)
        anchored = rf"\b{spaced}\b"
        compiled = re.compile(anchored, re.IGNORECASE)

        patterns.append(compiled)

    return patterns


# ── Compiled pattern lists ────────────────────────────────────────────────────

_COMPILED_NEGATIONS: list[re.Pattern] = _compile_patterns(_NEGATION_TERMS)
_COMPILED_LEGISLATION: list[re.Pattern] = _compile_patterns(_LEGISLATION_TERMS)

# Up to 10 whitespace-separated tokens between negation and legislative term.
# Prevents a match from bridging two unrelated sentences.
_WORD_GAP = r"(?:\s+\S+){0,10}\s+"

PATTERNS: list[re.Pattern] = [
    re.compile(
        # neg.pattern  → \b<negation_phrase>\b  (from _compile_patterns)
        # _WORD_GAP    → up to 10 intervening tokens + mandatory trailing whitespace
        # leg.pattern  → \b<legislation_term>\b (from _compile_patterns)
        rf"{neg.pattern}{_WORD_GAP}{leg.pattern}",
        re.IGNORECASE,
    )
    for neg in _COMPILED_NEGATIONS
    for leg in _COMPILED_LEGISLATION
]

## Safe but not future proof:
# REJECTION_REASONING_KEYWORDS = [
#     r"will not make legislation",
#     r"will not propose",
#     r"no legislative proposal",
#     r"no new legislation",
#     r"not to submit a legislative proposal",
#     r"no repeal of that legislation",
#     r"not necessary to propose a new legal",
#     r"not to submit legislation",
#     r"not propose legal",
#     r"no further legal acts",
# ]

# PATTERNS: list[re.Pattern] = [
#     re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
#     for keyword in REJECTION_REASONING_KEYWORDS
# ]

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
