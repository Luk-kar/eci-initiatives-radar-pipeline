"""Text formatting helpers for list partials."""

import re

import pandas as pd

from page_creator.partials.lists.utils.constants import DEFAULT_TRUNCATE


def truncate(text: str, max_len: int = DEFAULT_TRUNCATE) -> str:
    """Truncate ``text`` to ``max_len`` characters, appending '…' if cut; returns '' for NaN."""
    if pd.isna(text):
        return ""
    s = str(text)
    return s if len(s) <= max_len else s[: max_len - 1] + "…"


def wrap_initiative_title(title: str) -> str:
    """
    Transform an ECI initiative title for readable display in list rows and
    chart y-axis labels. Rules are applied left-to-right on every segment.

    Args:
        title: Raw initiative title string.
    """

    def _split_part(parts: list[str]) -> list[str]:
        result: list[str] = []

        for part in parts:
            remaining = part

            while len(remaining) > 50:
                cut = remaining.rfind(" ", 0, 50)
                if cut == -1:
                    # no space to split on, stop splitting this part
                    break
                result.append(remaining[:cut])
                remaining = remaining[cut + 1 :].lstrip()

            if remaining:
                result.append(remaining)

        return result

    def _merge_orphans(lines: list[str]) -> list[str]:
        """
        Merge a trailing orphan segment into the previous line when:
          - the orphan is â‰¤ _MIN_SEGMENT_WORDS words, AND
          - the preceding line is â‰¤ _MAX_HEAD_WORDS words
            (so we never create a new oversized line).
        """

        _MIN_SEGMENT_WORDS = 2  # a segment with â‰¤ this many words is an orphan
        _MAX_HEAD_WORDS = 5  # only merge if the head is also short enough to absorb it

        if len(lines) < 2:
            return lines

        merged: list[str] = [lines[0]]
        for segment in lines[1:]:
            orphan_words = len(segment.split())
            prev_words = len(merged[-1].split())
            if orphan_words <= _MIN_SEGMENT_WORDS and prev_words <= _MAX_HEAD_WORDS:
                merged[-1] = merged[-1] + " " + segment  # re-join with a space
            else:
                merged.append(segment)
        return merged

    def _truncate_if_too_long(text: str) -> str:
        """
        Final safety net â€” applied after all splitting and orphan-merging:

        1. If there are more than _MAX_LINES segments, keep only the first
           _MAX_LINES and append an ellipsis to the last kept line.
        2. If the joined string still exceeds _MAX_TOTAL_CHARS, trim the last
           kept line at the nearest word boundary below the remaining budget,
           then append an ellipsis.
        """
        _MAX_LINES = 4  # hard cap on number of \n-separated segments
        _MAX_TOTAL_CHARS = DEFAULT_TRUNCATE  # hard cap on total character length
        _ELLIPSIS = "…"

        lines = text.split("\n")

        # Rule 1: too many lines
        if len(lines) > _MAX_LINES:
            lines = lines[:_MAX_LINES]
            lines[-1] = lines[-1].rstrip(_ELLIPSIS) + _ELLIPSIS

        result = "\n".join(lines)

        # Rule 2: total character budget
        if len(result) > _MAX_TOTAL_CHARS:

            # How many chars are consumed by the newline tokens themselves?
            nl_overhead = len(lines) - 1  # each "\n" is 1 char
            char_budget = _MAX_TOTAL_CHARS - nl_overhead - len(_ELLIPSIS)

            # Rebuild from lines until we exhaust the budget
            kept: list[str] = []
            used = 0
            for line in lines:
                if used + len(line) <= char_budget:
                    kept.append(line)
                    used += len(line)
                else:
                    # Trim the current line to the remaining budget
                    remaining = char_budget - used
                    if remaining > 0:
                        cut = line.rfind(" ", 0, remaining)
                        trimmed = line[:cut] if cut != -1 else line[:remaining]
                        kept.append(trimmed.rstrip() + _ELLIPSIS)
                    else:
                        # No room at all â€” add ellipsis to last kept
                        if kept:
                            kept[-1] = kept[-1].rstrip() + _ELLIPSIS
                    break
            result = "\n".join(kept)

        return result

    if title is None:
        raise ValueError("wrap_initiative_title: title must not be None.")

    if not isinstance(title, str):
        raise TypeError(
            f"wrap_initiative_title: expected str, got {type(title).__name__!r}."
        )

    if not title.strip():
        raise ValueError(
            "wrap_initiative_title: title must not be empty or whitespace-only."
        )

    HTML_NEW_LINE = "<br>"

    segments_on_dots_etc = [s.strip() for s in re.split(r"[!;:.]", title) if s.strip()]
    title_new_lined = _split_part(segments_on_dots_etc)
    title_merged_orphans = _merge_orphans(title_new_lined)

    title_joined = HTML_NEW_LINE.join(title_merged_orphans)
    title_truncated = _truncate_if_too_long(title_joined)

    return title_truncated


def strip_markdown_links(text: str) -> str:
    """Replace Markdown inline links with their link text, preserving all other content.

    ``[Communication](https://ec.europa.eu/...)`` → ``Communication``

    Args:
        text: Raw string potentially containing ``[text](url)`` patterns.

    Returns:
        The input string with every inline Markdown link replaced by its
        display text. Returns an empty string for NaN or None values.
    """

    # ─── Markdown Link Pattern Fragments ─────────────────────────────────────────

    # Label part: one or more characters that are not [ or ]
    _MD_LABEL = r"[^\[\]]+"

    # URL part: non-paren characters, allowing one level of nested parentheses
    # e.g. matches C(2026)3225&lang=en without stopping at the inner `)`
    _MD_URL_SAFE_CHARS = r"[^()]*"  # chars with no parentheses
    _MD_URL_INNER_PAREN = r"\([^()]*\)"  # one (...) pair, nothing nested

    # URL pattern: start with plain non-paren chars, then allow zero or more
    # segments of "(...)" plus more non-paren chars. This lets URLs contain
    # a single level of parentheses (e.g. "C(2026)3225&lang=en") without
    # prematurely terminating the overall Markdown link match.
    _MD_URL = (
        _MD_URL_SAFE_CHARS + r"(?:" + _MD_URL_INNER_PAREN + _MD_URL_SAFE_CHARS + r")*"
    )

    # Full inline Markdown link: [label](url)
    _MARKDOWN_LINK_RE = re.compile(
        r"\[(" + _MD_LABEL + r")\]" r"\((" + _MD_URL + r")\)"
    )

    # ─────────────────────────────────────────────────────────────────────────────

    if not text or pd.isna(text):
        return ""

    return _MARKDOWN_LINK_RE.sub(r"\1", text)


def strip_boilerplate_headers(text: str) -> str:
    """
    Remove known boilerplate header lines (e.g. 'Main conclusions of the …:')
    from a multi-line description string.

    Args:
        text: Arbitrary multi-line string, potentially containing boilerplate
            headers at the start of lines.

    Returns:
        The input text with any matching header lines removed, preserving all
        other content and line breaks.
    """

    # Precompile patterns for the boilerplate header lines we want to remove

    _HEADER_LINE_PATTERNS = [
        # "Main conclusions of the Communication ." or "Main conclusions of the Communication:"
        re.compile(r"^Main conclusions of the.*[.:]\s*$", re.MULTILINE),
        # "The Commission commits to:" / "The Commission commits to :"
        re.compile(r"^The Commission commits to\s*[.:]\s*$", re.MULTILINE),
        # "Official document:" / "Official documents related to the decision:"
        re.compile(r"^Official document.*[.:]\s*$", re.MULTILINE),
        # "The Commission committed, in particular, to taking the following actions:"
        re.compile(r"^The Commission committed.*[.:]\s*$", re.MULTILINE),
    ]

    if not isinstance(text, str):
        raise TypeError(
            f"strip_boilerplate_headers: expected str, got {type(text).__name__!r}."
        )

    cleaned = text
    for pattern in _HEADER_LINE_PATTERNS:
        # Replace entire matching lines with the empty string
        cleaned = pattern.sub("", cleaned)

    # Optionally normalise multiple blank lines that may result
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned
