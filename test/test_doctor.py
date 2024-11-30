from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_create_doctor():
    payload = {
        "docid":"D000000001",
        "docname": "Shirokami Fubuki"
    }

    response = client.post("/doctor", json=payload)
    assert response.status_code == 201
    assert response.json().get("message") == "Doctor created successfully"

def test_update_doctor():
    payload = {
        "docid" : "D000000001",
        "docname" : "FubuKing" 
    }

    response = client.put("/doctor", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Doctor name updated successfully"
    assert response.json().get("doctor").get("docname") == payload["docname"]