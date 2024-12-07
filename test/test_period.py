from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_create_period():
    payload = {
        "perid" : "0000000000",
        "cid" : "C001",
        "weekday" : "1",
        "starttime" : "14:30",
        "endtime" : "18:30"
    }

    response = client.post("/period", json=payload)
    assert response.status_code == 201
    assert response.json().get("message") == "Period created successfully"

def test_update_period():
    payload = {
        "perid" : "0000000000",
        "available" : False
    }
    response = client.put("/period", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Period name updated successfully"
    updated = response.json().get("period")
    for key ,value in payload.items():
        assert updated.get(key) == value
