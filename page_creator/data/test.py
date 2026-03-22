import pandas as pd

df = pd.read_csv("./initiatives_2026-02-09_13-24-41.csv")

df = df.drop(columns=["primary_policy_area"])

df.to_csv("./initiatives_2026-02-09_13-24-41.csv", index=False)

# values = df["current_status"].unique()

print(df.columns)
