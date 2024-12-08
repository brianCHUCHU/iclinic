from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_create_reservation():
    payload = {
        "pid" : "",
        "sid" : "",
        "date" : "",
        "applytime" : "",
        "tid" : "",
        "status" : "",
        "attendance" : None
    }

    response = client.post("/reservation", json=payload)
    assert response.status_code == 201
    assert response.json().get("message") == "Reservation created successfully"

def test_update_reservation():
    payload = {
        "status" : ""
    }
    response = client.put("/reservation", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Reservation name updated successfully"
    updated = response.json().get("reservation")
    for key ,value in payload.items():
        assert updated.get(key) == value
