"""Renders a centred footer note showing the date the source data was last retrieved."""

from datetime import datetime


def generate_last_data_update(data_date: str) -> str:
    """Return an HTML footer snippet with the data retrieval date.

    Args:
        data_date: Date string in ``YYYY-MM-DD`` format, as produced by
                   ``_find_latest_csv`` in ``generate_charts.py``.

    Returns:
        An HTML ``<footer>`` string with a centred date note.

    Raises:
        ValueError: If ``data_date`` is not a valid ``YYYY-MM-DD`` string.
    """
    try:
        parsed = datetime.strptime(data_date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(
            f"Invalid data_date '{data_date}'. Expected format: YYYY-MM-DD."
        ) from exc

    formatted = parsed.strftime("%-d %b %Y")  # e.g. "9 Feb 2026"

    return (
        '<footer id="last-data-update-slot" class="data-timestamp">'
        f"Last data retrieved: {formatted}"
        "</footer>"
    )
