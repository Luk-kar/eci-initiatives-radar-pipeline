import pandas as pd

df = pd.read_csv("./initiatives_2026-02-09_13-24-41.csv")

values = df["current_status"].unique()
print(values)
