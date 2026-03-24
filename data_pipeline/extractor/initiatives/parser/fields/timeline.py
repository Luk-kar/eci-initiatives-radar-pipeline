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

    # If we still have no recognised timeline fields, raise an error
    if not timeline_data:
        raise FieldValueError(
            field="timeline",
            message=(
                "Cannot extract timeline: element was found but yielded no "
                "recognisable fields. Check that timeline title mappings in "
                "_normalize_timeline_title() cover the titles present in this page."
            ),
        )

    # Only now add full timeline JSON, once we know there is at least one
    # recognised field.
    if timeline_json_data:
        timeline_data["timeline"] = json.dumps(
            timeline_json_data, ensure_ascii=False, separators=(",", ":")
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
    - Prefer "Valid initiative" if present after "Verification"
    - Otherwise, take the first step containing "initiative" that comes after
      "Verification" and is either before "Answered initiative" or is the last item
    """
    verification_idx = None
    answered_idx = None

    # First pass: locate Verification and Answered initiative indices
    for idx, (title, _date) in enumerate(timeline_sequence):
        if title == "Verification":
            verification_idx = idx
        if title == "Answered initiative":
            answered_idx = idx

    if verification_idx is None:
        return timeline_data

    verification_end_candidate: Optional[Tuple[str, Optional[str]]] = None

    # Second pass: find the best candidate after Verification
    for idx, (title, date) in enumerate(timeline_sequence):
        if idx <= verification_idx:
            continue

        title_lower = title.lower()

        # Only consider steps mentioning "initiative"
        if "initiative" not in title_lower:
            continue

        # Must be before Answered (if present) or be the last item
        if (
            answered_idx is not None
            and idx >= answered_idx
            and idx != len(timeline_sequence) - 1
        ):
            continue

        # Prefer "Valid initiative" explicitly if found
        if title == "Valid initiative":
            verification_end_candidate = (title, date)
            break

        # Otherwise, if no candidate yet, take the first suitable one
        if verification_end_candidate is None:
            verification_end_candidate = (title, date)

    if verification_end_candidate:
        timeline_data["timeline_verification_end"] = verification_end_candidate[1]

    return timeline_data
