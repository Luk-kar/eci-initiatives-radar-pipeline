from bs4 import BeautifulSoup


def extract_current_status(self, soup: BeautifulSoup) -> str:
    """Extract current initiative current_status"""

    # Find the currently active timeline item
    current_status_element = soup.find(class_="ecl-timeline__item--current")

    if current_status_element:
        # Extract the status title from the timeline item
        status_title = current_status_element.find(class_="ecl-timeline__title")

        if status_title:
            # Return the raw status text without any mapping
            return status_title.get_text().strip()

    # No current status found in timeline
    return ""
