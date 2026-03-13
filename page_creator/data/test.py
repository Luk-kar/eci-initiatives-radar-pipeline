import pandas as pd

df = pd.read_csv("./initiatives.csv")

open_df = df[df["current_status"] == "Collection Ongoing"]
print(
    open_df[
        ["title", "timeline_collection_start", "timeline_collection_closed"]
    ].to_string()
)
