import pandas as pd

df = pd.read_json("data/raw_data/competitions.json")
df.to_csv("data/raw_data/competitions.csv", index=False)

df1 = pd.read_json("data/raw_data/events/15946.json")
df1.to_csv("data/raw_data/15946.csv")
print(df.head())
print(df.columns)
print(df.isnull())

print(df1.head())
print(df1.columns)
print(df1.isnull())
