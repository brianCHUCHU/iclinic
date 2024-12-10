from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_membership():
    payload = {
        "pid": "A179910536",
        "acct_pw": "password",
        "email": "123@gmail.com",
        "pname": "John Doe",
        "birthdate": "1990-01-01",
        "gender": "M",
        "status": "M"
    }
    response = client.post("/memberships", json=payload)
    assert response.json().get("message") == "Membership created successfully"
    assert response.status_code == 201

# def test_get_membership_by_id():
#     response = client.get("/memberships/T124488950")
#     assert response.status_code == 200
#     assert response.json().get("pid") == "T124488950"

# def test_update_membership():
#     payload = {
#         "pid": "T124488950",
#         "acct_pw": "securepassword",
#         "email": "ccccc@gmail.com"
#     }   
#     response = client.put("/memberships/T124488950", json=payload)
#     assert response.status_code == 200
#     assert response.json().get("message") == "Membership updated successfully"



# def test_authenticate_membership():
#     payload = {
#         "pid": "T124488950",
#         "acct_pw": "securepassword"
#     }
#     response = client.post("/memberships/authenticate", json=payload)
#     assert response.status_code == 200
#     assert response.json().get("message") == "Authentication successful"

