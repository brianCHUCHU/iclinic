from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

# def test_create_reservation():
#     payload = {
#         "pid" : "T124488950",
#         "sid" : "0000000000",
#         "date" : "2024-01-01",
#         "applytime" : "2020-05-11 20:50:30",
#         "tid" : "0000000000",
#         "status" : "P",
#         "attendance" : None
#     }

#     response = client.post("/reservation", json=payload)
#     assert response.status_code == 201
#     assert response.json().get("message") == "Reservation created successfully"

# def test_update_reservation():
#     payload = {
#         "pid" : "T124488950",
#         "sid" : "0000000000",
#         "date" : "2024-01-01",
#         "tid" : "0000000000",
#         "status" : "R"
#     }
#     response = client.put("/reservation", json=payload)
#     assert response.status_code == 200
#     assert response.json().get("message") == "Reservation name updated successfully"
#     updated = response.json().get("reservation")
#     for key ,value in payload.items():
#         assert updated.get(key) == value
