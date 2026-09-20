import numpy as np
import pandas as pd

from src.config import SCOUTING_FEATURES
from src.scouting.explanations import explain_similarity


def test_explanation_identifies_similar_and_different_features():
    profiles = []

    for player_id, name in [(1, "Target"), (2, "Candidate")]:
        row = {
            "player_id": player_id,
            "player_name": name,
            "role_group": "Midfielder",
            "primary_position_id": 13,
            "qualifying_matches": 30,
        }

        for feature in SCOUTING_FEATURES:
            row[feature] = 1.0

        profiles.append(row)

    player_profiles = pd.DataFrame(profiles)

    scaled_features = np.zeros((2, len(SCOUTING_FEATURES)))

    # Candidate is identical on everything except the first feature.
    scaled_features[1, 0] = 5.0

    most_similar, largest_differences = explain_similarity(player_profiles=player_profiles, scaled_features=scaled_features, target_player_id=1, candidate_player_id=2, top_n=3)

    assert SCOUTING_FEATURES[0] in largest_differences["feature"].values
    assert SCOUTING_FEATURES[0] not in most_similar["feature"].values
