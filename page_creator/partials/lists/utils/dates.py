"""Date normalisation helpers for list partials."""

import pandas as pd


def normalise_registration_date(df: pd.DataFrame) -> pd.DataFrame:
    """Parse and normalise the ``registration_date`` column to a human-readable string.

    Args:
        df: DataFrame with a ``registration_date`` column in ``DD/MM/YYYY`` format.

    Returns:
        The same DataFrame with ``registration_date`` converted to ``'1 Jan 2024'`` format.
    """
    df = df.copy()
    df["registration_date"] = pd.to_datetime(
        df["registration_date"], format="%d/%m/%Y"
    ).dt.strftime("%-d %b %Y")
    return df
