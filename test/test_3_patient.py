from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_patient():
    payload = {
        "pid": "T124488950",
        "pname": "John Doe",
        "birthdate": "1990-01-01",
        "gender": "M",
        "status": "A"
    }

    response = client.post("/patients", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Patient created successfully"
    assert response.json()["patient"]["pid"] == payload["pid"]

def test_get_patient_id():
    pid = "T124488950"
    response = client.get(f"/patients?pid={pid}")
    assert response.status_code == 200
    assert response.json()["patient"]["pid"] == pid

def test_get_patient_name():
    pname = "John Doe"
    response = client.get(f"/patients?pname={pname}")
    assert response.status_code == 200
    assert response.json()["patient"][0]["pname"] == pname

def test_update_patient():
    pid = "T124488950"
    payload = {
        "pname": "John Smith",
        "status": "I",
        'birthdate': "1990-01-01",
        'gender': "M",
    }

    response = client.put(f"/patients/{pid}", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Patient updated successfully"
    assert response.json()["patient"]["pname"] == payload["pname"]
    assert response.json()["patient"]["status"] == payload["status"]

# def test_delete_patient():
#     pid = "T124488950"
#     response = client.delete(f"/patients/{pid}")
#     assert response.status_code == 200
#     assert response.json()["message"] == "Patient deleted successfully"
#     assert response.json()["patient"]["pid"] == pid
