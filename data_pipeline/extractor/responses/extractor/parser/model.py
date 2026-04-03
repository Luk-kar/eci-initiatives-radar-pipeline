from typing import Optional, List

from pydantic import BaseModel


class ECIResponseParseHTMLRecord(BaseModel):
    """Parsed data record from the ECI initiative's response page."""

    # --- Extracted from response HTML ---
    commission_answer_text: Optional[List[str]] = None
    followup_url: Optional[str] = None

    # List fields — serialized as JSON strings for flat CSV compatibility
    followup_events: Optional[List[str]] = None  # plain-text descriptions with links
