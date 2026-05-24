# Renders a scrollable table of ECI initiatives that failed the
# Member State signature verification stage.
import pandas as pd

from page_creator.partials.styles.colors import KpiColors as colors
from page_creator.partials.lists.utils.sort import sort_by_registration_date
from page_creator.partials.lists.utils import (
    build_card_title,
    generate_sig_threshold_card,
)

STATUS = "Insufficient Verified Signatures"


def filter(df: pd.DataFrame) -> pd.DataFrame:
    """Filter for initiatives that failed post-collection verification.

    Args:
        df: The full ECI initiatives DataFrame.

    Returns:
        Filtered DataFrame containing only STATUS rows.
    """

    return df[df["current_status"] == STATUS]


def sort(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise dates and sort by registration date descending.

    Args:
        df: Filtered DataFrame of verification-failed initiatives.

    Returns:
        Sorted and date-normalised DataFrame.
    """

    return sort_by_registration_date(df)


def generate_insufficient_verified_signatures(df: pd.DataFrame) -> str:
    """Return an HTML card containing a table of ECIs that failed
    post-collection signature verification.

    Filters for rows with current_status == STATUS, sorted by registration
    date descending. Each row shows the initiative title linked to its page,
    the registration date, a truncated objective, a signature progress bar,
    and a country-threshold progress bar.

    Args:
        df: The full ECI initiatives DataFrame. Must contain current_status,
            title, initiative_url, objective, registration_date,
            signatures_collected, and signatures_countries_threshold_met_count
            columns.

    Returns:
        An HTML string wrapping the table in a card div, or a card with a
        fallback message if no initiatives match.
    """

    SUBTITLE = "Signatures collected, but failed Member State verification."

    color = colors.insufficient_verified_signatures
    df_sorted = sort(filter(df))
    title = build_card_title("🔎", STATUS, len(df_sorted), color, subtitle=SUBTITLE)

    return generate_sig_threshold_card(
        df_sorted,
        title,
        color,
        empty_message="No initiatives failed at the verification stage.",
    )
