import re

NEGATION_TERMS = [
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


def normalise(text: str) -> str:
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

    _MARKDOWN_LINK_REGEX: re.Pattern = re.compile(r"\[([^\]]+)\]\([^)]+\)")

    return _MARKDOWN_LINK_REGEX.sub(r"\1", text)


def compile_patterns(terms: list[str]) -> list[re.Pattern]:
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
