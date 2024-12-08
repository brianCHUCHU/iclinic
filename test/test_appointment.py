from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_create_appointment():
    payload = {
        "pid" : "",
        "sid" : "",
        "date" : "",
        "order" : "",
        "applytime" : "",
        "status" : "",
        "attendence" : None
    }

    response = client.post("/appointment", json=payload)
    assert response.status_code == 201
    assert response.json().get("message") == "Appointment created successfully"

def test_update_appointment():
    payload = {
        "status" : ""
    }
    response = client.put("/appointment", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Appointment name updated successfully"
    updated = response.json().get("appointment")
    for key ,value in payload.items():
        assert updated.get(key) == value
