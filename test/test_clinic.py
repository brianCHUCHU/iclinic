from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_clinic():
    payload = {
        "cid": "C001",
        "fee": 500,
        "queue_type": 'I',
        "acct_name": "clinic_admin",
        "acct_pw": "securepassword",
        "cname": "Best Clinic",
        "city": "Taipei",
        "district": "Da'an",
        "address": "123 Health St."
    }
    response = client.post("/clinics", json=payload)
    assert response.status_code == 201
    assert response.json().get("message") == "Clinic created successfully"
