"""
Shared HTML validation and save utilities.
"""

import os

import html5lib
from html5lib.html5parser import ParseError
from bs4 import BeautifulSoup

from .consts import MIN_HTML_LENGTH


def validate_html(page_source: str, min_length: int | None = None) -> None:
    """Validate HTML using html5lib.

    Raises ValueError if too short, ParseError if parse issues are detected.
    """

    threshold = min_length if min_length is not None else MIN_HTML_LENGTH
    if len(page_source) < threshold:
        raise ValueError(
            f"HTML content too short: {len(page_source)} characters (min {threshold})"
        )

    try:
        # parse() in html5lib 1.1 does NOT support strict=True,
        # so we just call it and catch ParseError.
        html5lib.parse(
            page_source,
            treebuilder="etree",
            namespaceHTMLElements=False,
        )
    except ParseError as e:
        # re-raise so callers can decide what to do
        raise e


def save_html(path: str, page_source: str) -> None:
    """
    Prettify and save HTML to disk.

    Assumes the HTML was already validated by validate_html() upstream.

    Args:
        path: Destination file path.
        page_source: Raw HTML string.
    """

    os.makedirs(os.path.dirname(path), exist_ok=True)
    soup = BeautifulSoup(page_source, "html.parser")
    pretty_html = soup.prettify()

    with open(path, "w", encoding="utf-8") as f:
        f.write(pretty_html)
