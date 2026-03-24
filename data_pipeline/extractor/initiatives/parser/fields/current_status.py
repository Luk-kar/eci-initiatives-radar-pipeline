from bs4 import BeautifulSoup


from ....extractor_shared.errors import FieldValueError


def extract_current_status(soup: BeautifulSoup) -> str:
    """Extract current initiative status from the active timeline item.

    Raises:
        FieldValueError: If no active timeline item is found, or if the active
            item contains no title element.
    """
    current_status_element = soup.find(class_="ecl-timeline__item--current")

    if not current_status_element:
        raise FieldValueError(
            field="current_status",
            message=(
                "Cannot extract current status: no active timeline item "
                "('ecl-timeline__item--current') found in page."
            ),
        )

    status_title = current_status_element.find(class_="ecl-timeline__title")

    if not status_title:
        raise FieldValueError(
            field="current_status",
            message=(
                "Cannot extract current status: active timeline item found but "
                "contains no title element ('ecl-timeline__title')."
            ),
        )

    return status_title.get_text().strip()
