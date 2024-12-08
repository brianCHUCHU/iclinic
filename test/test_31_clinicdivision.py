from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_create_client_division():
    response = client.post(
        "/clinicdivision/create",
        json={
            "divid":"D01",
            "cid":"C001",
            "available": True
        }
    )
    assert response.status_code == 201
    assert response.json().get("message") == "Clinic division created successfully"

def test_enable_clinic_division():
    response = client.put(
        "/clinicdivision/enable",
        json={
            "divid":"D01",
            "cid":"C001"
        }
    )
    assert response.status_code == 200
    assert response.json().get("message") == "Clinic division enabled successfully"
    assert response.json().get("clinic_division").get("available") == True

def test_disable_clinic_division():
    response = client.put(
        "/clinicdivision/disable",
        json={
            "divid":"D01",
            "cid":"C001"
        }
    )
    assert response.status_code == 200
    assert response.json().get("message") == "Clinic division disabled successfully"
    assert response.json().get("clinic_division").get("available") == False

def test_delete_clinic_division():
    response = client.request(
        "DELETE",
        "/clinicdivision/delete",
        json={
            "divid": "D01",
            "cid": "C001"
        }
    )
    assert response.status_code == 200
    assert response.json().get("message") == "Clinic division deleted successfully"

    