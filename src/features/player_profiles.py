import pandas as pd

from src.config import SCOUTING_FEATURES, MIN_QUALIFYING_MINUTES, MIN_QUALIFYING_MATCHES

def add_per_90_features(player_match_df: pd.DataFrame) -> pd.DataFrame:
    player_match_df = player_match_df.copy()

    count_features = {
        "total_passes": "passes_per_90",
        "progressive_passes": "progressive_passes_per_90",
        "total_carries": "carries_per_90",
        "progressive_carries": "progressive_carries_per_90",
        "total_dribbles": "dribbles_per_90",
        "total_shots": "shots_per_90",
        "goals": "goals_per_90",
        "total_xg": "xg_per_90",
        "total_duels": "duels_per_90",
        "successful_duels": "successful_duels_per_90",
    }

    for count_column, per_90_column in count_features.items():
        player_match_df[per_90_column] = (player_match_df[count_column] / player_match_df["minutes_played"] * 90)

    return player_match_df


def build_player_profiles(player_match_df: pd.DataFrame) -> pd.DataFrame:
    player_match_df = player_match_df[player_match_df["minutes_played"] >= MIN_QUALIFYING_MINUTES].copy()
    player_match_df = add_per_90_features(player_match_df)

    matches_played = player_match_df.groupby("player_id").agg(qualifying_matches=("match_id", "nunique")).reset_index()
    features = player_match_df.groupby("player_id")[SCOUTING_FEATURES].mean().reset_index()
    player_metadata = player_match_df[["player_id", "player_name", "role_group", "primary_position_id"]].drop_duplicates(subset="player_id").reset_index(drop=True)

    player_profiles = player_metadata.merge(features, on="player_id", how="inner")
    player_profiles = player_profiles.merge(matches_played, on="player_id", how="inner")
    player_profiles = player_profiles[player_profiles["qualifying_matches"] >= MIN_QUALIFYING_MATCHES].reset_index(drop=True)

    print("Rows after 20-minute filter: ", len(player_match_df))
    return player_profiles
