import pandas as pd
import pytest

from src.config import SCOUTING_FEATURES
from src.scouting.recommender import PlayerRecommender


def make_profiles():
    players = [
        {
            "player_id": 1,
            "player_name": "Target",
            "role_group": "Midfielder",
            "primary_position_id": 13,
            "qualifying_matches": 30,
        },
        {
            "player_id": 2,
            "player_name": "Very Similar",
            "role_group": "Midfielder",
            "primary_position_id": 13,
            "qualifying_matches": 25,
        },
        {
            "player_id": 3,
            "player_name": "Less Similar",
            "role_group": "Midfielder",
            "primary_position_id": 10,
            "qualifying_matches": 40,
        },
        {
            "player_id": 4,
            "player_name": "Defender",
            "role_group": "Defender",
            "primary_position_id": 3,
            "qualifying_matches": 50,
        },
    ]

    for feature in SCOUTING_FEATURES:
        players[0][feature] = 1.0
        players[1][feature] = 1.1
        players[2][feature] = 2.0
        players[3][feature] = 1.05

    return pd.DataFrame(players)


def test_target_player_is_excluded():
    recommender = PlayerRecommender(make_profiles())

    results = recommender.find_similar_players(player_id=1, top_n=10, position_filter=None)
    assert 1 not in results["player_id"].values


def test_results_are_sorted_by_distance():
    recommender = PlayerRecommender(make_profiles())

    results = recommender.find_similar_players(player_id=1, top_n=3, position_filter=None)
    assert results["distance"].is_monotonic_increasing


def test_role_filter_only_returns_same_role():
    recommender = PlayerRecommender(make_profiles())

    results = recommender.find_similar_players(player_id=1, top_n=10, position_filter="role")
    assert (results["role_group"] == "Midfielder").all()

def test_position_filter_only_returns_same_position():
    recommender = PlayerRecommender(make_profiles())

    results = recommender.find_similar_players(player_id=1, top_n=10, position_filter="position")
    assert (results["primary_position_id"] == 13).all()


def test_closest_player_is_ranked_first():
    recommender = PlayerRecommender(make_profiles())

    results = recommender.find_similar_players(player_id=1, top_n=3, position_filter=None)
    assert results.iloc[0]["player_id"] == 4


def test_unknown_player_raises_error():
    recommender = PlayerRecommender(make_profiles())

    with pytest.raises(ValueError):
        recommender.find_similar_players(player_id=999)


def test_invalid_position_filter_raises_error():
    recommender = PlayerRecommender(make_profiles())

    with pytest.raises(ValueError):
        recommender.find_similar_players(player_id=1, position_filter="banana")
