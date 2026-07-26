import pandas as pd
import json
from pathlib import Path
import argparse


def parse_event_files(event_files):
    events_list = []
    passes_list = []
    shots_list = []
    carries_list = []
    dribbles_list = []
    duels_list = []

    for item in event_files:
        match_id = int(item.stem)

        with open(item, "r") as f:
            event_data = json.load(f)

        for event in event_data:
            location = event.get("location")
            player = event.get("player")
            position = event.get("position")

            event_dict = {
                "match_id": match_id,
                "event_id": event["id"],
                "event_index": event["index"],
                "period": event["period"],
                "timestamp": event["timestamp"],
                "minute": event["minute"],
                "second": event["second"],
                "possession": event["possession"],
                "possession_team_id": event["possession_team"]["id"],
                "team_id": event["team"]["id"],
                "position_id": position["id"] if position else None,
                "duration": event.get("duration"),
                "under_pressure": event.get("under_pressure"),
                "event_type": event["type"]["name"],
                "player_id": player["id"] if player else None,
                "location_x": location[0] if location else None,
                "location_y": location[1] if location else None
            }

            events_list.append(event_dict)

            if event["type"]["name"] == "Pass":
                pass_data = event.get("pass") or {}
                recipient = pass_data.get("recipient") or {}
                end_location = pass_data.get("end_location")

                pass_outcome = pass_data.get("outcome") or {}

                passes_dict = {
                    "event_id": event["id"],
                    "recipient_id": recipient.get("id"),
                    "length": pass_data.get("length"),

                    "outcome_id": pass_outcome.get("id"),

                    "end_location_x": end_location[0] if end_location else None,
                    "end_location_y": end_location[1] if end_location else None
                }

                passes_list.append(passes_dict)

            if event["type"]["name"] == "Shot":
                shot_data = event.get("shot") or {}

                outcome = shot_data.get("outcome")
                technique = shot_data.get("technique")
                body_part = shot_data.get("body_part")
                shot_type = shot_data.get("type")
                end_location = shot_data.get("end_location")

                shots_dict = {
                    "event_id": event["id"],
                    "statsbomb_xg": shot_data["statsbomb_xg"],
                    "key_pass_id": shot_data.get("key_pass_id"),
                    "outcome_id": outcome["id"] if outcome else None,
                    "first_time": shot_data.get("first_time"),
                    "technique_id": technique["id"] if technique else None,
                    "body_part_id": body_part["id"] if body_part else None,
                    "shot_type_id": shot_type["id"] if shot_type else None,
                    "end_location_x": end_location[0] if end_location else None,
                    "end_location_y": end_location[1] if end_location and len(end_location) > 1 else None,
                    "end_location_z": end_location[2] if end_location and len(end_location) > 2 else None
                }

                shots_list.append(shots_dict)

            if event["type"]["name"] == "Carry":
                carry_data = event.get("carry") or {}

                carries_dict = {
                    "event_id": event["id"],
                    "end_location_x": carry_data["end_location"][0],
                    "end_location_y": carry_data["end_location"][1],
                }

                carries_list.append(carries_dict)

            if event["type"]["name"] == "Dribble":
                dribble_data = event.get("dribble") or {}
                outcome = dribble_data.get("outcome")

                dribbles_dict = {
                    "event_id": event["id"],
                    "nutmeg": dribble_data.get("nutmeg"),
                    "outcome_id": outcome["id"] if outcome else None,
                }

                dribbles_list.append(dribbles_dict)

            if event["type"]["name"] == "Duel":
                duel_data = event.get("duel") or {}
                duel_type = duel_data.get("type")

                duels_dict = {
                    "event_id": event["id"],
                    "duel_type_id": duel_type["id"] if duel_type else None
                }

                duels_list.append(duels_dict)

    events_df = pd.DataFrame(events_list, columns=["match_id", "event_id", "event_index", "period", "timestamp", "minute", "second", "possession", "possession_team_id",
            "team_id", "position_id", "duration", "under_pressure", "event_type", "player_id", "location_x", "location_y"])
    passes_df = pd.DataFrame(passes_list, columns=["event_id", "recipient_id", "length", "outcome_id", "end_location_x", "end_location_y"])
    shots_df = pd.DataFrame(shots_list, columns=["event_id", "statsbomb_xg", "key_pass_id", "outcome_id", "first_time",
            "technique_id", "body_part_id", "shot_type_id", "end_location_x", "end_location_y", "end_location_z"])
    carries_df = pd.DataFrame(carries_list, columns=["event_id", "end_location_x", "end_location_y"])
    dribbles_df = pd.DataFrame(dribbles_list, columns=["event_id", "nutmeg", "outcome_id"])
    duels_df = pd.DataFrame(duels_list, columns=["event_id", "duel_type_id"])

    return {
        "events": events_df,
        "passes": passes_df,
        "shots": shots_df,
        "carries": carries_df,
        "dribbles": dribbles_df,
        "duels": duels_df,
    }


def process_events_in_batches(events_dir, output_dir, batch_size=10, max_batches=None):
    events_dir = Path(events_dir)
    output_dir = Path(output_dir)

    if not events_dir.is_dir():
        raise FileNotFoundError(f"Events directory does not exist: {events_dir.resolve()}")

    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero")

    event_files = sorted(events_dir.glob("*.json"))

    if not event_files:
        raise FileNotFoundError(f"No JSON event files found in: {events_dir.resolve()}")

    output_dir.mkdir(parents=True, exist_ok=True)

    existing_parquet_files = list(output_dir.glob("*.parquet"))

    if existing_parquet_files:
        raise FileExistsError("Output directory already contains Parquet files: "f"{output_dir.resolve()}")

    for batch_number, start in enumerate(range(0, len(event_files), batch_size)):
        if (max_batches is not None and batch_number >= max_batches):
            break

        batch_files = event_files[start:start + batch_size]

        tables = parse_event_files(batch_files)

        row_counts = ",".join(f"{table_name}={len(dataframe)}" for table_name, dataframe in tables.items())

        for table_name, dataframe in tables.items():
            output_path = (output_dir/f"{table_name}_{batch_number:04d}.parquet")

            dataframe.to_parquet(output_path, index=False)

        print(f"Batch {batch_number}: " f"{len(batch_files)} files, "f"{row_counts}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse StatsBomb events data")

    parser.add_argument("--data_dir", required=True, help="Path to the events data directory")
    parser.add_argument("--output_dir", required=True, help="Path to the directory for the processed events files")
    parser.add_argument("--batch_size", type=int, default=100, help="Batch size for event data processing")
    parser.add_argument("--max_batches", type=int, default=None, help="Maximum number of batches to be processed")

    args = parser.parse_args()

    process_events_in_batches(args.data_dir, args.output_dir, args.batch_size, args.max_batches)
