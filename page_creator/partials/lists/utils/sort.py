"""Shared sorting utilities for list partials."""

import pandas as pd


def sort_by_registration_date(df: pd.DataFrame) -> pd.DataFrame:
    """Parse and sort a DataFrame by registration_date descending.

    Converts ``registration_date`` from a day-first string to ``datetime.date``,
    sorts descending (most recent first), and resets the index.

    Args:
        df: Must contain a ``registration_date`` column in ``DD/MM/YYYY`` format.

    Returns:
        A sorted copy with ``registration_date`` as ``datetime.date``.
    """
    df = df.copy()
    df["registration_date"] = pd.to_datetime(
        df["registration_date"], dayfirst=True
    ).dt.date
    return df.sort_values("registration_date", ascending=False).reset_index(drop=True)
