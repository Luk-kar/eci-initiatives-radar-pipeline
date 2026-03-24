from bs4 import BeautifulSoup


def extract_objective(soup: BeautifulSoup) -> str:
    """Extract initiative objectives (max 1,100 characters)"""

    # Find objectives section
    objectives_section = soup.find("h2", string=re.compile(r"Objectives?", re.I))
    if objectives_section:
        objective_text = ""
        next_element = objectives_section.find_next_sibling()
        while next_element and next_element.name != "h2":
            if next_element.name == "p":
                objective_text += next_element.get_text().strip() + " "
            next_element = next_element.find_next_sibling()

        return objective_text.strip()[: ContentLimits.OBJECTIVE_MAX_LENGTH]

    return ""
