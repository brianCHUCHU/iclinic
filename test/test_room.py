from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

# def test_create_room():
#     payload = {
#         "rid":"R000000001",
#         "cid":"C001",
#         "rname": "100"
#     }

#     response = client.post("/room", json=payload)
#     assert response.status_code == 201
#     assert response.json().get("message") == "Room created successfully"


# def test_update_room():
#     payload = {
#         "rid" : "R000000001",
#         "cid":"C001",
#         "rname" : "200" 
#     }

#     response = client.put("/room", json=payload)
#     assert response.status_code == 200
#     assert response.json().get("message") == "Room name updated successfully"
#     assert response.json().get("room").get("rname") == payload["rname"]

# payload = {
#     "rid": "R001",
#     "cid": "C001",
#     "rname": "Test Room"
# }

# payload = {
#     "rid": "R001",

# }

# def test_get_room_by_rid(client):
#     # 查詢房間
#     response = client.get(f"/rooms?rid={valid_room_data['rid']}")
    
#     assert response.status_code == 200
#     assert response.json()["rooms"][0]["rid"] == valid_room_data["rid"]
#     assert response.json()["rooms"][0]["cid"] == valid_room_data["cid"]
#     assert response.json()["rooms"][0]["rname"] == valid_room_data["rname"]