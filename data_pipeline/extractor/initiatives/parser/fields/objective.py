import re

from bs4 import BeautifulSoup

from ...consts import ContentLimits
from ....extractor_shared.errors import FieldValueError


def extract_objective(soup: BeautifulSoup) -> str:
    """Extract initiative objectives (max 1,100 characters).

    Raises:
        FieldValueError: If no objectives section is found, or if the section
            contains no extractable paragraph text.
    """

    objectives_section = soup.find("h2", string=re.compile(r"Objectives?", re.I))

    if not objectives_section:
        raise FieldValueError(
            field="objective",
            message="Cannot extract objective: no 'Objectives' heading found in page.",
        )

    objective_text = ""
    next_element = objectives_section.find_next_sibling()

    while next_element and next_element.name != "h2":

        if next_element.name == "p":
            objective_text += next_element.get_text().strip() + " "

        next_element = next_element.find_next_sibling()

    objective_text = objective_text.strip()

    if not objective_text:

        raise FieldValueError(
            field="objective",
            message=(
                "Cannot extract objective: 'Objectives' heading was found but "
                "contains no paragraph text before the next section."
            ),
        )

    return objective_text[: ContentLimits.OBJECTIVE_MAX_LENGTH]
