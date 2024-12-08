from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_create_appointment():
    payload = {
        "pid" : "T124488950",
        "sid" : "0000000000",
        "date" : "2024-01-01",
        "order" : 2,
        "applytime" : "2020-05-11 20:50:30",
    }

    response = client.post("/appointment", json=payload)
    assert response.status_code == 201
    assert response.json().get("message") == "Appointment created successfully"

def test_update_appointment():
    payload = {
        "pid" : "T124488950",
        "sid" : "0000000000",
        "date" : "2024-01-01",
        "order" : 2,
        "status" : "P"
    }
    response = client.put("/appointment", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Appointment name updated successfully"
    updated = response.json().get("appointment")
    for key ,value in payload.items():
        assert updated.get(key) == value
