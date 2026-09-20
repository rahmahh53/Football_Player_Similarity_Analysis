import json
from pathlib import Path

import pandas as pd


def time_to_seconds(time_string: str) -> int:
    minute, seconds = time_string.split(":")
    return int(minute) * 60 + int(seconds)


def calculate_player_minutes(positions: list, match_end_time: str) -> float:
    match_end = time_to_seconds(match_end_time)
    intervals = []

    for position in positions:
        start = max(0, time_to_seconds(position["from"]))
        end = match_end if position["to"] is None else min(time_to_seconds(position["to"]), match_end)

        if end > start:
            intervals.append((start, end))

    if not intervals:
        return 0

    intervals.sort()
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]

        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return sum(end - start for start, end in merged) / 60


def build_player_minutes(lineup_dir: Path, event_dir: Path) -> pd.DataFrame:
    player_minutes = []

    for lineup_file in lineup_dir.iterdir():
        with open(lineup_file, "r") as file:
            lineup_data = json.load(file)

        match_id = int(lineup_file.stem)
        event_file = event_dir / f"{match_id}.json"

        with open(event_file, "r") as file:
            event_data = json.load(file)

        half_end_events = [event for event in event_data if event["type"]["name"] == "Half End" and event["period"] <= 4]
        last_half_end = max(half_end_events, key=lambda event: (event["period"], event["minute"], event["second"]))
        match_end_time = f"{last_half_end['minute']}:{last_half_end['second']:02d}"

        for team in lineup_data:
            team_id = team["team_id"]

            for player in team["lineup"]:
                if not player["positions"]:
                    continue

                minutes_played = calculate_player_minutes(player["positions"], match_end_time)

                player_minutes.append({
                    "player_id": player["player_id"],
                    "team_id": team_id,
                    "match_id": match_id,
                    "minutes_played": minutes_played,
                })

    return pd.DataFrame(player_minutes)
