import pandas as pd
import ast
import json


def merge_eci_followups(csv_path1: str, csv_path2: str) -> pd.DataFrame:
    """
    Concatenates two ECI CSV files and merges the followup_events lists
    for duplicate registration numbers without dropping data.
    """
    # Read both CSVs and concatenate them
    df1 = pd.read_csv(csv_path1)
    df2 = pd.read_csv(csv_path2)
    df_combined = pd.concat([df1, df2], ignore_index=True)

    def combine_event_lists(series):

        combined = []

        for item in series.dropna():

            if isinstance(item, str) and item.strip().startswith("["):

                try:
                    # Try parsing as JSON first
                    parsed = json.loads(item)
                    combined.extend(parsed)

                except json.JSONDecodeError:

                    try:
                        # Fallback for Python stringified lists (single quotes)
                        parsed = ast.literal_eval(item)

                        if isinstance(parsed, list):
                            combined.extend(parsed)
                        else:
                            combined.append(item)

                    except (ValueError, SyntaxError):
                        combined.append(item)
            else:
                combined.append(item)

        # Remove exact duplicates while preserving the order
        unique_combined = list(dict.fromkeys(combined))
        return unique_combined if unique_combined else None

    # Group by registration number and combine the events from both CSVs
    merged_df = df_combined.groupby("registration_number", as_index=False).agg(
        {"followup_events": combine_event_lists}
    )

    return merged_df[["registration_number", "followup_events"]].sort_values(
        by="registration_number"
    )


# Usage example:
eci_responses = (
    "data_pipeline/data/2026-04-09_15-38-52/eci_responses_2026-04-09_16-22-24.csv"
)
eci_responses_followup = "data_pipeline/data/2026-04-09_15-38-52/eci_responses_followup_2026-04-09_16-23-29.csv"
df_merged = merge_eci_followups(eci_responses, eci_responses_followup)
df_merged.to_csv("contacted.csv")
