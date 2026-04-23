"""
law_passed.py
-------------
Regex patterns and extractor for the ``Law_Passed`` output column.

``extract(text_items)`` scans each item in the combined text list for evidence
that a piece of EU legislation was adopted, applied, or entered into force and
returns the list of matched items (original strings), or ``None`` when nothing fired.
"""

from __future__ import annotations

import logging
import re

from .utils.pattern_utils import normalise, compile_patterns, NEGATION_TERMS

logger = logging.getLogger(__name__)

# ── Shared legislative vocabulary ─────────────────────────────────────────────

NON_EXPLICIT_MENTIONED_LEGISLATION = [r"new minimum hygiene standards?"]

# Based on scope restriction, we only want regulations, directives, and generic legal
# placeholder acts. We explicitly exclude decisions, recommendations, and opinions.
_LEGISLATION = [
    r"regulations?",
    r"directives?",
    r"(?:legislative |legal )?acts?", # |delegated |implementing
    r"legislations?",
    r"laws?",
    r"(?:legal |legislative )?instruments?",
    r"(?:legislative )?proposals?",
    r"amendments?",
    r"revisions?",
    r"rules?",
    r"codes?"
] + NON_EXPLICIT_MENTIONED_LEGISLATION

_FALSE_POSITIVE_LEGISLATION = ["proposal to adopt"]


# Verb/action lists
_VERBS = [
    r"appl(?:y|ies|ied|ying|icable)", # ication
    r"enter(?:ed|s|ing)?\s+(?:into\s+force|in(?:to)?\s+application)",
    r"force(?:d|s)?\s+into",
    r"repeal(?:ed|s)?",
    r"adopt(?:ed|s|ing)?",
    # r"implement(?:ed|s|ing)?",
    # r"implementation(?!\s+reports?)",
    r"came\s+into\s+force",
    r"became\s+applicable",
    # r"application(?!\s+of\s+the\s+(?:rules|directive|regulation))",
    r"publish(?:ed|s|ing)?\s+in\s+(?:the\s+)?Official\s+Journal"
]

_COMPILED_NEGATIONS: list[re.Pattern] = compile_patterns(NEGATION_TERMS)
_COMPILED_LEGISLATION: list[re.Pattern] = compile_patterns(_LEGISLATION)
_COMPILED_VERBS: list[re.Pattern] = compile_patterns(_VERBS)

# Up to 20 whitespace-separated tokens between verb and legislation or vice-versa
_WORD_GAP = r"(?:\s+\S+){0,30}\s+"

# Compile permutations of Verb + Gap + Legislation and Legislation + Gap + Verb
LAW_PASSED_PATTERNS: list[re.Pattern] = []

for verb_pattern in _COMPILED_VERBS:
    for leg_pattern in _COMPILED_LEGISLATION:
        # Verb before legislation
        LAW_PASSED_PATTERNS.append(
            re.compile(
                rf"{verb_pattern.pattern}{_WORD_GAP}{leg_pattern.pattern}",
                re.IGNORECASE,
            )
        )
        # Legislation before verb
        LAW_PASSED_PATTERNS.append(
            re.compile(
                rf"{leg_pattern.pattern}{_WORD_GAP}{verb_pattern.pattern}",
                re.IGNORECASE,
            )
        )


def _split_into_sentences(text: str) -> list[str]:
    """
    Splits text into sentence chunks to evaluate negations locally,
    while ignoring periods in common abbreviations.
    """
    # Mask common abbreviations to prevent incorrect splits
    text = re.sub(r'\bi\.e\.', 'i<dot>e<dot>', text, flags=re.IGNORECASE)
    text = re.sub(r'\be\.g\.', 'e<dot>g<dot>', text, flags=re.IGNORECASE)
    text = re.sub(r'\betc\.', 'etc<dot>', text, flags=re.IGNORECASE)
    
    # Split by period, exclamation, or question mark followed by whitespace
    chunks = re.split(r"(?<=[.!?])\s+", text)
    
    # Restore the masked dots and filter empty strings
    restored_chunks = []
    for c in chunks:
        if not c.strip():
            continue
        c = c.replace('i<dot>e<dot>', 'i.e.')
        c = c.replace('e<dot>g<dot>', 'e.g.')
        c = c.replace('etc<dot>', 'etc.')
        restored_chunks.append(c)
        
    return restored_chunks


def extract(text_items: list[str], rejected_legislation: bool = False) -> list[str] | None:
    """
    Scan *text_items* for indications that a law was passed/active.

    The matching evaluates text in chunks (sentences). If any chunk within
    an item matches the law-passed patterns AND is not negated by NEGATION_TERMS,
    the *entire original item* is appended to the result list.

    Args:
        text_items: Pre-merged list of text fragments for one initiative.

    Returns:
        ``list[str]`` of original text items when at least one matches,
        ``None`` otherwise.
    """
    if not text_items:
        return None

    matched_items: list[str] = []

    for item in text_items:
        if not item.strip():
            continue

        normalised_item = normalise(item)
        sentences = _split_into_sentences(normalised_item)

        item_matched = False

        for sentence in sentences:
            # Check if this sentence has a law passed trigger
            sentence_has_match = any(p.search(sentence) for p in LAW_PASSED_PATTERNS)

            if sentence_has_match:
                # Check for negations within the same sentence
                is_negated = any(neg.search(sentence) for neg in _COMPILED_NEGATIONS)

                # Exclude future conditional "will" or "expected" commonly used for proposals
                # This prevents "we will propose a regulation" from triggering
                future_conditional = bool(
                    re.search(
                        r"\b(?:will|expected to|proposes? to|proposal to adopt)\b",
                        sentence,
                        re.IGNORECASE,
                    )
                )

                if not is_negated and not future_conditional:
                    logger.debug("LAW_PASSED hit in sentence: %.80s", sentence)
                    item_matched = True
                    break  # Found a valid hit in this item, no need to check other sentences

        if item_matched:
            matched_items.append(item)

    return matched_items if matched_items else None
