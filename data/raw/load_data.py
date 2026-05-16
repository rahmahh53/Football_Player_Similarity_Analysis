import pandas as pd

df = pd.read_json("data/competitions.json")
df.to_csv("competitions.csv", index=False)

print(df.head())
print(df.columns)
print(df.isnull())
