"""Text formatting helpers for list partials."""

import pandas as pd

from page_creator.partials.lists.utils.constants import DEFAULT_TRUNCATE


def truncate(text: str, max_len: int = DEFAULT_TRUNCATE) -> str:
    """Truncate ``text`` to ``max_len`` characters, appending '…' if cut; returns '' for NaN."""
    if pd.isna(text):
        return ""
    s = str(text)
    return s if len(s) <= max_len else s[: max_len - 1] + "…"
