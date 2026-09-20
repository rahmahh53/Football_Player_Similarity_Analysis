import os
from pathlib import Path

from sqlalchemy import create_engine

from src.data.repository import load_player_match_features, merge_player_minutes
from src.features.player_minutes import build_player_minutes
from src.features.player_profiles import build_player_profiles


OUTPUT_PATH = Path("data/processed/scouting_profiles.parquet")


def main():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set.")

    db_engine = create_engine(database_url, pool_pre_ping=True)

    try:
        print("Loading player-match features...")
        player_match_df = load_player_match_features(db_engine)

        print("Calculating player minutes...")
        player_minutes_df = build_player_minutes(lineup_dir=Path("data/raw_data/lineups"), event_dir=Path("data/raw_data/events")        )

        print("Merging minutes...")
        player_match_df = merge_player_minutes(player_match_df, player_minutes_df)

        print("Building scouting profiles...")
        player_profiles = build_player_profiles(player_match_df)

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        player_profiles.to_parquet(OUTPUT_PATH, index=False)

        print(f"Saved {len(player_profiles):,} player profiles")
        print(f"Artifact: {OUTPUT_PATH}")

    finally:
        db_engine.dispose()


if __name__ == "__main__":
    main()
