from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

# def test_create_room():
#     payload = {
#         "rid":"R000000001",
#         "cid":"C000000001",
#         "rname": "100"
#     }

#     response = client.post("/room", json=payload)
#     assert response.status_code == 201
#     assert response.json().get("message") == "Room created successfully"


# def test_update_room():
#     payload = {
#         "rid" : "R000000001",
#         "cid":"C000000001",
#         "rname" : "200",
#         "available" : False
#     }

#     response = client.put("/room", json=payload)
#     assert response.status_code == 200
#     assert response.json().get("message") == "Room name updated successfully"
#     assert response.json().get("room").get("rname") == payload["rname"]

# def test_get_rooms_by_rid():
#     # 測試根據 rid 查詢
#     response = client.get("/rooms", params={"rid": "R000000001"})
#     assert response.status_code == 200
#     data = response.json()
#     assert "rooms" in data
#     assert len(data["rooms"]) > 0  # 確保返回的結果不為空
#     assert data["rooms"][0]["rid"] == "R000000001"  # 確保房間的 rid 是 R000000001

# def test_get_rooms_by_cid():
#     # 測試根據 cid 查詢
#     response = client.get("/rooms", params={"cid": "C001"})
#     assert response.status_code == 200
#     data = response.json()
#     assert "rooms" in data
#     assert len(data["rooms"]) > 0  # 確保返回的結果不為空
#     assert data["rooms"][0]["cid"] == "C001"  # 確保房間的 cid 是 C001

# def test_get_rooms_by_rname():
#     # 測試根據 rname 查詢
#     response = client.get("/rooms", params={"rname":"200"})
#     assert response.status_code == 200
#     data = response.json()
#     assert "rooms" in data
#     assert len(data["rooms"]) > 0  # 確保返回的結果不為空
#     assert data["rooms"][0]["rname"] == "200"  # 確保房間的名稱是 200

# def test_update_room_queue_number():
#     payload = {
#         "rid": "R000000001",
#         "queuenumber": 1,
#         "lastupdate": "2021-01-01 12:00:00"
#     }

#     response = client.put("/room/queuenumber", json=payload)
#     assert response.status_code == 200
#     assert response.json().get("message") == "Room queue number updated successfully"
#     assert response.json().get("room").get("rid") == payload["rid"]
#     assert response.json().get("room").get("queuenumber") == payload["queuenumber"]
# def test_get_room_queue_number():
#     # 測試獲取房間的排隊號碼
#     response = client.get("/room/queuenumber/R000000001", params={"rid": "R000000001"})
#     assert response.status_code == 200
#     assert response.json().get("queuenumber") == 1