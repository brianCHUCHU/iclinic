from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# def test_create_doctor():
#     payload = {
#         "docid":"D000000001",
#         "docname": "Shirokami Fubuki"
#     }

#     response = client.post("/doctor", json=payload)
#     assert response.status_code == 201
#     assert response.json().get("message") == "Doctor created successfully"

# def test_update_doctor():
#     payload = {
#         "docid" : "D000000001",
#         "docname" : "FubuKing" 
#     }

#     response = client.put("/doctor", json=payload)
#     assert response.status_code == 200
#     assert response.json().get("message") == "Doctor name updated successfully"
#     assert response.json().get("doctor").get("docname") == payload["docname"]

def test_create_hire():
    payload = {
        "docid": "T124488950",
        'docname': 'Shirokami Fubuki',
        "cid": "C001",
        "divid": "D01",
        "startdate": "2022-01-01"
    }

    response = client.post("/hire", json=payload)
    assert response.status_code == 201
    assert response.json().get("message") == ("Hire created successfully")
    assert response.json().get('hire').get("startdate") == payload["startdate"]

def test_update_hire():
    payload = {
        "docid": "T124488950",
        "cid": "C001",
        "divid": "D01",
        "enddate": "2022-12-31"
    }

    response = client.post("/hire", json=payload)
    print(response.json())
    assert response.status_code == 201
    assert response.json().get("message") == "Hire updated successfully"
    assert response.json().get('hire').get("enddate") == payload["enddate"]