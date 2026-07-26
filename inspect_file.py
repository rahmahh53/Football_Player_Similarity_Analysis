import pandas as pd
import json
from pathlib import Path

file_path = Path("data/raw_data/lineups")
sample_file = next(file_path.iterdir())

with open(sample_file, "r") as file:
    data = json.load(file)

# lineup1 = pd.DataFrame(data)
team_lineup = data[0]["lineup"]
# print(type(team_lineup))
# print(team_lineup[0])

players_df = pd.DataFrame(team_lineup)
# print(players_df.columns.tolist())
# print(players_df.head())

# print(players_df["country"][0])
# print(players_df[players_df["cards"].notna()].iloc[1]["cards"])
# print(players_df[players_df["positions"].notna()].iloc[0]["positions"]

