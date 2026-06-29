import logging

from bs4 import BeautifulSoup

from ....extractor_shared.errors import FieldValueError

logger = logging.getLogger(__name__)


def extract_current_status(soup: BeautifulSoup) -> str:
    """Extract current initiative status from the active timeline item.

    Falls back to the last timeline item with a non-empty title when no item
    is marked as current (e.g. corrupted source page).

    Raises:
        FieldValueError: If no timeline items exist at all, if the active
            item contains no title element, or if no non-empty title exists
            in any timeline item.
    """
    current_item = soup.find(class_="ecl-timeline__item--current")

    if current_item:
        return _title_from_current_item(current_item)

    items = soup.find_all(class_="ecl-timeline__item")

    if not items:
        raise FieldValueError(
            field="current_status",
            message=(
                "Cannot extract current status: no active timeline item "
                "('ecl-timeline__item--current') found in page."
            ),
        )

    return _fallback_status(items)


def _title_from_current_item(item) -> str:
    """Return the title text from a marked --current timeline item.

    Raises:
        FieldValueError: If the item has no title element.
    """

    title = item.find(class_="ecl-timeline__title")

    if not title:
        raise FieldValueError(
            field="current_status",
            message=(
                "Cannot extract current status: active timeline item found but "
                "contains no title element ('ecl-timeline__title')."
            ),
        )

    return title.get_text().strip()


def _fallback_status(items) -> str:
    """Recover status when no item carries the --current marker.

    Tries the last item with a non-empty title. Raises if none found.

    Raises:
        FieldValueError: If no non-empty title exists in any timeline item.
    """

    logger.warning(
        "⚠️ Cannot extract current status: no active timeline item "
        "('ecl-timeline__item--current') found in page. "
        "Falling back to last non-empty title in timeline."
    )

    title = _last_nonempty_title(items)

    if title:
        return title

    raise FieldValueError(
        field="current_status",
        message=(
            "⛔ Cannot extract current status: no non-empty title found "
            "in any timeline item ('ecl-timeline__title')."
        ),
    )


def _last_nonempty_title(items) -> str | None:
    """Return the last timeline title text that is not blank, or None."""

    for item in reversed(items):

        title = item.find(class_="ecl-timeline__title")

        if title and title.get_text(strip=True):
            return title.get_text().strip()

    return None