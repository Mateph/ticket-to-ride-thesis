from fastapi.testclient import TestClient

from main import app, store

client = TestClient(app)


def test_get_map():
    response = client.get("/api/map")
    assert response.status_code == 200
    assert "cities" in response.json()


def test_succesful_claim():
    payload = {"player_name": "apple", "route_id": "bud-vie-1"}

    response = client.post("/api/claim", json=payload)
    assert response.status_code == 200


def test_bad_message_400():
    payload = {"player_name": "cherry", "route_id": "bud-vie-1"}

    response = client.post("/api/claim", json=payload)
    assert response.status_code == 400


def test_missing_field_422():
    payload = {"route_id": "bud-vie-1"}

    response = client.post("/api/claim", json=payload)
    assert response.status_code == 422
