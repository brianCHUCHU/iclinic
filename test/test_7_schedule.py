from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

# def test_create_schedule():
#     payload = {
#         "sid" : "0000000000",
#         "divid" : "D01",
#         "perid" : "0000000000",
#         "docid" : "T124488950",
#     }

#     response = client.post("/schedule", json=payload)
#     assert response.status_code == 201
#     assert response.json().get("message") == "Schedule created successfully"

# def test_update_schedule():
#     payload = {
#         "sid" : "0000000000",
#         "docid" : "T124488950",
#         "available" : False
#     }
#     response = client.put("/schedule", json=payload)
#     assert response.status_code == 200
#     assert response.json().get("message") == "Schedule updated successfully"
#     assert response.json().get("schedule").get("available") == payload["available"]