# from fastapi.testclient import TestClient
# from main import app
# client = TestClient(app)

# def test_create_treatment():
#     payload = {
#         "tid" : "0000000000",
#         "docid" : "0000000000",
#         "divid" : "0000000000",
#         "cid" : "0000000000",
#         "tname" : "test"
#     }

#     response = client.post("/treatment", json=payload)
#     assert response.status_code == 201
#     assert response.json().get("message") == "Treatment created successfully"

# def test_update_treatment():
#     payload = {
#         "tid" : "0000000000",
#         "tname" : "200" ,
#         "available" : "0"
#     }
#     response = client.put("/treatment", json=payload)
#     assert response.status_code == 200
#     assert response.json().get("message") == "Treatment name updated successfully"
#     assert response.json().get("treatment").get("tname") == payload["tname"]