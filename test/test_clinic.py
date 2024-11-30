import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# def test_create_clinic():
#     payload = {
#         "cid": "C001",
#         "fee": 500,
#         "queue_type": 'I',
#         "acct_name": "clinic_admin",
#         "acct_pw": "securepassword",
#         "cname": "Best Clinic",
#         "city": "Taipei",
#         "district": "Da'an",
#         "address": "123 Health St."
#     }
#     response = client.post("/clinics", json=payload)
#     assert response.status_code == 201
#     assert response.json().get("message") == "Clinic created successfully"

# # test update
# def test_update_clinic():
#     payload = {
#         "cid": "C001",
#         "fee": 600,
#         "queue_type": 'I',
#         "acct_name": "clinic_admin",
#         "acct_pw": "securepassword",
#         "cname": "Best Clinic",
#         "city": "Taipei",
#         "district": "Da'an",
#         "address": "123 Health St."
#     }
#     response = client.put("/clinics/C001", json=payload)
#     assert response.status_code == 200
#     assert response.json().get("message") == "Clinic updated successfully"

# # test delete
# def test_delete_clinic():
#     response = client.delete("/clinics/C001")
#     assert response.status_code == 200
#     assert response.json().get("message") == "Clinic deleted successfully"

# test get clinic by id
def test_get_clinic_by_id():
    response = client.get("/clinics/C001")
    assert response.status_code == 200
    assert response.json().get("cid") == "C001"

def test_get_clinic_by_invalid_id():
    response = client.get("/clinics/invalid")
    assert response.status_code == 404
    assert response.json().get("detail") == "Clinic not found"

