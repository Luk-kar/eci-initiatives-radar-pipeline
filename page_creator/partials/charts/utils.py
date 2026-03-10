"""Shared HTML-formatting helpers for Plotly hover tooltips across chart partials."""

import textwrap


_WRAP_WIDTH = 60
_MAX_LINES = 6
_MAX_HOVER_ITEMS = 10


def hover_item_list(titles: list[str], max_items: int = _MAX_HOVER_ITEMS) -> str:
    """Return a ``<br>``-joined bullet list of titles, truncated to ``max_items`` with a count suffix."""

    if not titles:
        return "None"

    items = [f"• {t}" for t in titles[:max_items]]
    result = "<br>".join(items)

    if len(titles) > max_items:
        result += f"<br><i>… (and {len(titles) - max_items} more)</i>"

    return result


def hover_wrap(text: str, width: int = _WRAP_WIDTH, max_lines: int = _MAX_LINES) -> str:
    """Break long text into ``<br>``-separated lines, truncating to ``max_lines`` with a trailing '…'."""

    lines = textwrap.wrap(str(text), width=width)

    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip() + "…"

    return "<br>".join(lines)
