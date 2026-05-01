import re

# Pre-compile the regex for performance
_NEWLINE_RE = re.compile(r"\n+")


def normalize_newlines(text: str) -> str:
    """Collapse multiple consecutive newlines into a single newline."""

    return _NEWLINE_RE.sub("\n", text)
