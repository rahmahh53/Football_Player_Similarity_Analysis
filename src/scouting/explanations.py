import numpy as np
import pandas as pd

from src.config import SCOUTING_FEATURES


def explain_similarity(player_profiles: pd.DataFrame, scaled_features: np.ndarray, target_player_id: int, candidate_player_id: int, top_n: int = 5):
    target_idx = player_profiles.index[player_profiles["player_id"] == target_player_id][0]
    candidate_idx = player_profiles.index[player_profiles["player_id"] == candidate_player_id][0]

    target_vector = scaled_features[target_idx]
    candidate_vector = scaled_features[candidate_idx]

    differences = np.abs(target_vector - candidate_vector)

    comparison = pd.DataFrame({
        "feature": SCOUTING_FEATURES,
        "target_value": player_profiles.loc[target_idx, SCOUTING_FEATURES].to_numpy(),
        "candidate_value": player_profiles.loc[candidate_idx, SCOUTING_FEATURES].to_numpy(),
        "standardized_difference": differences,
    })

    most_similar = comparison.sort_values("standardized_difference").head(top_n)
    largest_differences = comparison.sort_values("standardized_difference", ascending=False).head(top_n)

    return most_similar, largest_differences
