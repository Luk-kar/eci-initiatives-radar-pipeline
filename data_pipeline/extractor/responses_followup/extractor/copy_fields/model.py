from pydantic import BaseModel


class ECIResponseInheritedRecord(BaseModel):
    """Inherited data record from the ECI initiative's entry page."""

    # --- Core metadata (copied from responses_list.csv) ---
    initiative_url: str
    response_url: str
    followup_url: str
    registration_number: str
    title: str
