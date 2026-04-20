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

REJECTED_PATTERNS: list[re.Pattern] = [
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

# REJECTED_PATTERNS: list[re.Pattern] = [
#     re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
#     for keyword in REJECTION_REASONING_KEYWORDS
# ]

# ── The Commissions tabling law commitment  ───────────────────────────────────

# ── Proposal terms ────────────────────────────────────────────────────────────
# Matches a legislative root followed (within _WORD_GAP) by a proposal-surface noun.
# e.g. "legislative proposal", "legal act", "legal directive", "legislative measure"

_PROPOSAL_ROOT = r"proposals?|directives?|regulations?|acts?|changes?|measures?"

PROPOSAL_PATTERN: re.Pattern = re.compile(
    rf"\b(?:{_LEGAL}|{_LEGISLATIVE_FORMS}){_WORD_GAP}(?:{_PROPOSAL_ROOT})\b",
    re.IGNORECASE,
)

# ── Non-rejection guard ───────────────────────────────────────────────────────

# NON_REJECTION reuses _COMPILED_NEGATIONS: an item is a commitment when it
# contains PROPOSAL_PATTERN AND none of the negation patterns fire on it.
NON_REJECTION: list[re.Pattern] = _COMPILED_NEGATIONS


# ── Commitment check ──────────────────────────────────────────────────────────


def check_tabling_law_committed(text_items: list[str], skip_item: str) -> bool:
    """
    Check whether ANY OTHER item in *text_items* mentions a legislative/proposal
    term WITHOUT a negation — i.e. a commitment rather than a rejection.

    ``skip_item`` is the normalised item that already triggered the rejection
    hit; it is excluded so the same sentence cannot cancel itself.

    Args:
        text_items: Pre-merged list of text fragments for one initiative.
        skip_item:  The normalised item that fired the rejection pattern.

    Returns:
        ``True`` if another item commits to legislation, ``False`` otherwise.
    """
    for item in text_items:

        normalised = _normalise(item).strip()

        if not normalised or normalised == skip_item:
            continue

        if not PROPOSAL_PATTERN.search(normalised):
            continue

        # Commitment only if no negation term fires on the same item
        is_negated = any(p.search(normalised) for p in NON_REJECTION)

        if not is_negated:
            logger.debug("LAW_COMMITTED hit in: %.80s", normalised)
            return True

    return False


# ── Extractor ─────────────────────────────────────────────────────────────────


def extract(text_items: list[str]) -> bool:
    """
    Scan *text_items* for REJECTED_LEGISLATION and LAW_COMMITTED signals.

    Pass 1 — rejection: iterate items, set flag on first hit, then stop.
    Pass 2 — commitment: only runs when rejection was found; iterates all
              OTHER items for a legislative commitment (PROPOSAL_PATTERN
              present, no NON_REJECTION negation).

    Args:
        text_items: Pre-merged list of text fragments for one initiative.

    Returns:
        ``True``  — rejection found, no commitment in any other item.
        ``False`` — no rejection found, OR rejection overridden by commitment.
    """
    rejected_item: str | None = None

    # ── Pass 1: find the first rejection ─────────────────────────────────────
    for item in text_items:

        normalised = _normalise(item).strip()

        if not normalised:
            continue

        if any(p.search(normalised) for p in REJECTED_PATTERNS):

            logger.debug("REJECTED_LEGISLATION hit in: %.80s", normalised)
            rejected_item = normalised
            break

    if rejected_item is None:
        return False

    # ── Pass 2: check for commitment in any OTHER item ────────────────────────
    committed = check_tabling_law_committed(text_items, skip_item=rejected_item)

    if committed:
        logger.debug(
            "REJECTED_LEGISLATION overridden: commitment found in another item"
        )
        return False

    return True
