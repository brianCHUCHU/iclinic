from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_create_room():
    payload = {
        "rid":"R000000001",
        "cid":"C001",
        "rname": "100"
    }

    response = client.post("/room", json=payload)
    assert response.status_code == 201
    assert response.json().get("message") == "Room created successfully"


def test_update_room():
    payload = {
        "rid" : "R000000001",
        "cid":"C001",
        "rname" : "200" 
    }

    response = client.put("/room", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Room name updated successfully"
    assert response.json().get("room").get("rname") == "200"