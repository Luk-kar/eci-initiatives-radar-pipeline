import pandas as pd

df = pd.read_csv("./initiatives.csv")

values = df["current_status"].unique()
print(values)
