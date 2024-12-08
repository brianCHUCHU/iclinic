from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_create_room_schedule():
    response = client.post(
        "/roomschedule/create",
        json={
            "rid":"R000000001",
            "cid":"C001",
            "sid" : "0000000000",
            "available": True
        }
    )
    assert response.status_code == 201
    assert response.json().get("message") == "Room schedule created successfully"

def test_enable_room_schedule():
    response = client.put(
        "/roomschedule/enable",
        json={
            "rid":"R000000001",
            "cid":"C001",
            "sid" : "0000000000"
        }
    )
    assert response.status_code == 200
    assert response.json().get("message") == "Room schedule enabled successfully"
    assert response.json().get("room_schedule").get("available") == True

def test_disable_room_schedule():
    response = client.put(
        "/roomschedule/disable",
        json={
            "rid":"R000000001",
            "cid":"C001",
            "sid" : "0000000000"
        }
    )
    assert response.status_code == 200
    assert response.json().get("message") == "Room schedule disabled successfully"
    assert response.json().get("room_schedule").get("available") == False

def test_delete_room_schedule():
    response = client.request(
        "DELETE",
        "/roomschedule/delete",
        json={
            "rid": "R000000001",
            "cid": "C001",
            "sid": "0000000000"
        }
    )
    assert response.status_code == 200
    assert response.json().get("message") == "Room schedule deleted successfully"
