from pydantic import BaseModel


class ECIInitiativeInheritedRecord(BaseModel):
    """Inherited data record from the ECI initiative's entry page."""

    # --- Core metadata (copied from responses_list.csv) ---
    response_url: str
    initiative_url: str
    registration_number: str
    title: str
