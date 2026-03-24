from typing import Optional, List, Tuple, Dict
import re
import json

from bs4 import BeautifulSoup

from ....extractor_shared.errors import FieldValueError


def extract_timeline_data(soup: BeautifulSoup) -> dict[str, Optional[str]]:
    """Extract timeline information from ECL timeline.

    Raises:
        FieldValueError: If no timeline element is found in the page, or if
            the timeline contains no recognisable fields after processing.
    """

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
        normalized_title = _normalize_timeline_title(title)

        if normalized_title:
            timeline_data[normalized_title] = content

    # Post-process timeline_verification_end based on sequence
    timeline_data = _process_verification_end(timeline_sequence, timeline_data)

    # Add full timeline as JSON string
    if timeline_json_data:
        timeline_data["timeline"] = json.dumps(
            timeline_json_data, ensure_ascii=False, separators=(",", ":")
        )

    if not timeline_data:
        raise FieldValueError(
            field="timeline",
            message=(
                "Cannot extract timeline: element was found but yielded no "
                "recognisable fields. Check that timeline title mappings in "
                "normalize_timeline_title() cover the titles present in this page."
            ),
        )

    return timeline_data


def _normalize_timeline_title(title: str) -> Optional[str]:
    """Normalize timeline titles to standard field names"""

    # Add more mappings as needed
    title_mapping = {
        "Registered": "timeline_registered",
        "Collection start date": "timeline_collection_start_date",
        "Collection closed": "timeline_collection_closed",
        "Verification": "timeline_verification_start",
        "Answered initiative": "timeline_response_commission_date",
        "Collection ongoing": "timeline_collection_start_date",  # Map ongoing to start date
        "Registration": "timeline_registered",
    }

    return title_mapping.get(title)


def _process_verification_end(
    timeline_sequence: List[Tuple[str, Optional[str]]],
    timeline_data: Dict[str, Optional[str]],
) -> Dict[str, Optional[str]]:
    """
    Determine timeline_verification_end based on sequence rules:
    - Accept 'Valid initiative'
    - Accept any step containing 'initiative' that comes after 'Verification'
    and is last OR comes before 'Answered initiative'
    """

    # Find indices in timeline
    verification_idx = None
    answered_idx = None
    verification_end_candidate = None

    for idx, (title, date) in enumerate(timeline_sequence):
        title_lower = title.lower()

        # Track Verification position
        if title == "Verification":
            verification_idx = idx

        # Track Answered initiative position
        if title == "Answered initiative":
            answered_idx = idx

        # Check for any title containing 'initiative' after verification
        if verification_idx is not None and "initiative" in title_lower:

            # Only consider if it's after Verification
            if idx > verification_idx:

                # Check if it's before Answered or is the last item
                if (
                    answered_idx is None
                    or idx < answered_idx
                    or idx == len(timeline_sequence) - 1
                ):
                    verification_end_candidate = (title, date)

    # Set timeline_verification_end if we found a valid candidate
    if verification_end_candidate:
        timeline_data["timeline_verification_end"] = verification_end_candidate[1]

    return timeline_data
