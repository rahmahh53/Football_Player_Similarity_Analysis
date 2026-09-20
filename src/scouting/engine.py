import pandas as pd

from src.config import DEFAULT_TOP_N
from src.scouting.recommender import PlayerRecommender
from src.scouting.explanations import explain_similarity


class ScoutingEngine:
    def __init__(self, player_profiles: pd.DataFrame):
        self.recommender = PlayerRecommender(player_profiles)

    def find_replacements(self, player_id: int, top_n: int = DEFAULT_TOP_N, position_filter: str | None = "role", explanation_features: int = 3) -> list[dict]:
        recommendations = self.recommender.find_similar_players(player_id=player_id, top_n=top_n, position_filter=position_filter)
        results = []
        for _, candidate in recommendations.iterrows():
            most_similar, largest_differences = explain_similarity(player_profiles=self.recommender.player_profiles, scaled_features=self.recommender.scaled_features, target_player_id=player_id, candidate_player_id=candidate["player_id"], top_n=explanation_features)
            results.append({
                "player_id": int(candidate["player_id"]),
                "player_name": candidate["player_name"],
                "role_group": candidate["role_group"],
                "primary_position_id": int(candidate["primary_position_id"]),
                "qualifying_matches": int(candidate["qualifying_matches"]),
                "distance": round(float(candidate["distance"]), 3),
                "most_similar_features": most_similar["feature"].tolist(),
                "largest_differences": largest_differences["feature"].tolist(),
            })

        return results
