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


verb_rejecting = []

negation = []

legal_noun = []


REJECTION_REASONING_KEYWORDS = [
    r"\b(?:decid[a-z]{1,3} not|not (?:mak[a-z]{1,3}|propos[a-z]{1,3}))\s.+?legisla[a-z]+\b",
    "no legislative proposal",
    "no new legislation",
    "no repeal\b.+\blegisla[a-z]+\b",
    "not to submit\b.+\blegisla[a-z]+\b",
    "(outside|beyond)\b.+\competence",
    "not.+propose.+legal",
]

_SENTENCE_SPLIT_RE: re.Pattern = re.compile(r"[.;:'\"\u2013\u2014]+")


def _split_sentences(text: str) -> list[str]:
    """
    Split *text* on sentence-ending and clause-separating punctuation
    (``.``, ``;``, ``:``, ``'``, ``"``, ``–``, ``—``) and return only
    non-empty stripped fragments.

    Args:
        text: A single normalised text fragment.

    Returns:
        List of sub-sentences ready for pattern matching.
    """
    return [s.strip() for s in _SENTENCE_SPLIT_RE.split(text) if s.strip()]


PATTERNS: list[re.Pattern] = [
    re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
    for keyword in REJECTION_REASONING_KEYWORDS
]

# ── Extractor ─────────────────────────────────────────────────────────────────


def extract(text_items: list[str]) -> bool:
    """
    Scan *text_items* for REJECTED_LEGISLATION pattern matches.

    Each item is first normalised (Markdown links stripped), then split into
    sub-sentences on ``.``, ``;``, ``:``, ``'``, ``"`` and em/en-dashes so
    that a keyword spanning a clause boundary cannot produce a false positive.
    Evaluation stops at the first match (short-circuit).

    Args:
        text_items: Pre-merged list of text fragments for one initiative.

    Returns:
        ``True`` when at least one pattern fires, ``False`` otherwise.
    """
    for item in text_items:

        normalised = _normalise(item).strip()

        if not normalised:
            continue

        for sentence in _split_sentences(normalised):

            for pattern in PATTERNS:

                if pattern.search(sentence):

                    logger.debug(
                        "REJECTED_LEGISLATION hit: %r in: %.80s",
                        pattern.pattern,
                        sentence,
                    )

                    return True
    return False
