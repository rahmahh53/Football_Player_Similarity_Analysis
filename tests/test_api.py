from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["players_loaded"] == 1633


def test_xavi_replacements():
    response = client.get("/players/20131/replacements", params={"top_n": 5, "position_filter": "role"})

    assert response.status_code == 200

    data = response.json()
    recommendations = data["recommendations"]

    assert len(recommendations) == 5
    assert recommendations[0]["player_name"] == "Thiago Motta"
    assert recommendations[0]["distance"] == 2.832
    assert all(player["role_group"] == "Midfielder" for player in recommendations)


def test_list_players():
    response = client.get("/players")

    assert response.status_code == 200

    players = response.json()

    assert len(players) == 1633
    assert {"player_id", "player_name", "role_group"} <= players[0].keys()

    xavi = next(player for player in players if player["player_id"] == 20131)

    assert xavi["player_name"] == "Xavier Hernández Creus"
    assert xavi["role_group"] == "Midfielder"


def test_get_player_profile():
    response = client.get("/players/20131/profile")

    assert response.status_code == 200

    player = response.json()

    assert player["player_id"] == 20131
    assert player["player_name"] == "Xavier Hernández Creus"
    assert player["role_group"] == "Midfielder"
    assert "passes_per_90" in player
    assert "progressive_passes_per_90" in player

def test_get_player_percentiles():
    response = client.get("/players/20131/percentiles")

    assert response.status_code == 200

    data = response.json()

    assert data["player_id"] == 20131
    assert len(data["percentiles"]) == 15

    assert all(
        0 <= value <= 100
        for value in data["percentiles"].values()
    )
