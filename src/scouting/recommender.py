import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.config import SCOUTING_FEATURES, DEFAULT_TOP_N

class PlayerRecommender:
    def __init__(self, player_profiles: pd.DataFrame):
        self.player_profiles = player_profiles.reset_index(drop=True)
        self.scaler = StandardScaler()
        self.scaled_features = self.scaler.fit_transform(self.player_profiles[SCOUTING_FEATURES])

    def find_similar_players(self, player_id: int, top_n: int= DEFAULT_TOP_N, position_filter: str| None = "role") -> pd.DataFrame:

        if player_id not in self.player_profiles["player_id"].values:
            raise ValueError(f"Player {player_id} is not in the scouting population.")
        if position_filter not in ["role", "position", None]:
            raise ValueError("position_filter must be 'role', 'position', or None.")

        target_row = self.player_profiles[self.player_profiles["player_id"] == player_id]
        target_idx = target_row.index[0]
        target_vector = self.scaled_features[target_idx]

        target_role = target_row["role_group"].iloc[0]
        candidates = self.player_profiles.copy()
        candidate_vectors = self.scaled_features.copy()

        if position_filter == "role":
           target_role = target_row["role_group"].iloc[0]
           mask = candidates["role_group"] == target_role
           candidates = candidates[mask].copy()
           candidate_vectors = candidate_vectors[mask.to_numpy()]

        elif position_filter == "position":
           target_position = target_row["primary_position_id"].iloc[0]
           mask = candidates["primary_position_id"] == target_position
           candidates = candidates[mask].copy()
           candidate_vectors = candidate_vectors[mask.to_numpy()]

        candidates["distance"] = np.linalg.norm(candidate_vectors - target_vector, axis=1)
        candidates = candidates[candidates["player_id"] != player_id].copy()
        candidates = candidates.sort_values("distance").head(top_n)

        return candidates[["player_id", "player_name", "role_group", "primary_position_id", "qualifying_matches", "distance"]].reset_index(drop=True)
