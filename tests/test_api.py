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
