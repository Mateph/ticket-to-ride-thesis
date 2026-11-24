import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(autouse=True)
def fresh_game(reset_game_state):
    pass


client = TestClient(app)


def test_get_map():
    response = client.get("/api/map")
    assert response.status_code == 200
    assert "cities" in response.json()


def test_succesful_claim():
    valid_data = {"player_name": "apple", "route_id": "bud-vie-1"}

    response = client.post("/api/claim", json=valid_data)
    assert response.status_code == 200


def test_bad_message_400():
    valid_data = {"player_name": "cherry", "route_id": "bud-vie-1"}

    response = client.post("/api/claim", json=valid_data)
    assert response.status_code == 400


def test_missing_field_422():
    invalid_data = {"route_id": "bud-vie-1"}

    response = client.post("/api/claim", json=invalid_data)
    assert response.status_code == 422
