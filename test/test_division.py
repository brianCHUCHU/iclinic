import pytest
from fastapi.testclient import TestClient
from main import app  # 假設你的 FastAPI 應用位於 main.py

client = TestClient(app)

# Test data for division
valid_division_data = {
    "divid": "D01",
    "divname": "內科"
}


def test_create_division():
    response = client.post("/divisions", json=valid_division_data)
    assert response.status_code == 201
    assert response.json()["divname"] == valid_division_data["divname"]


def test_get_division_by_id():
    division_id = valid_division_data["divid"]

    response = client.get(f"/divisions?divid={division_id}")
    assert response.status_code == 200
    assert response.json()["divid"] == division_id

def test_get_non_existent_division():
    response = client.get("/divisions?divid=invalid")
    assert response.status_code == 404
    assert response.json()["detail"] == "Division not found"

def test_get_division_by_name():
    division_name = valid_division_data["divname"]

    response = client.get(f"/divisions?divname={division_name}")
    assert response.status_code == 200
    assert response.json()["divname"] == division_name

def test_get_non_existent_division_by_name():
    response = client.get("/divisions?divname=invalid")
    assert response.status_code == 404
    assert response.json()["detail"] == "Division not found"