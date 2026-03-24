from typing import Optional
from bs4 import BeautifulSoup


def extract_timeline_data(soup: BeautifulSoup) -> dict[str, Optional[str]]:
    """Extract timeline information from ECL timeline"""

    timeline_data = {}

    # Find the timeline container
    timeline = soup.find("ol", class_="ecl-timeline")
    if not timeline:
        return timeline_data

    # Extract all timeline items
    timeline_items = timeline.find_all("li", class_="ecl-timeline__item")

    # Track timeline order for verification end logic AND for full timeline JSON
    timeline_sequence = []
    timeline_json_data = []

    for item in timeline_items:
        # Extract title
        title_element = item.find("div", class_="ecl-timeline__title")
        if not title_element:
            continue

        title = title_element.get_text().strip()
        # Remove red asterisk marker if present
        title = re.sub(r"<span[^>]*>.*?</span>", "", title)
        title = title.replace("*", "").strip()

        # Extract content (date) if available
        content_element = item.find("div", class_="ecl-timeline__content")
        content = content_element.get_text().strip() if content_element else None

        # Store sequence for verification end processing
        timeline_sequence.append((title, content))

        # NEW: Store for full timeline JSON
        timeline_json_data.append({"step": title, "date": content})

        # Normalize title to match our field names
        normalized_title = self._normalize_timeline_title(title)

        if normalized_title:
            timeline_data[normalized_title] = content

    # Post-process timeline_verification_end based on sequence
    timeline_data = self._process_verification_end(timeline_sequence, timeline_data)

    # Add full timeline as JSON string
    if timeline_json_data:
        timeline_data["timeline"] = json.dumps(
            timeline_json_data, ensure_ascii=False, separators=(",", ":")
        )

    return timeline_data
