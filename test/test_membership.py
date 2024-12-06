import pytest
from fastapi.testclient import TestClient
import sys
import os

# 確保添加項目根目錄到 Python 搜索路徑
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
print(f"Adding root directory to sys.path: {root_dir}")
sys.path.append(root_dir)

from main import app

client = TestClient(app)

def test_create_membership():
    payload = {
        "pid": "P001",
        "acctname": "member_user",
        "acctpw": "securepassword",
        "email": "user@example.com"
    }
    response = client.post("/membership", json=payload)
    print(response.status_code, response.json())  # 調試輸出
    assert response.status_code == 201
    assert response.json().get("pid") == "P001"
    assert response.json().get("acctname") == "member_user"

# test update membership
def test_update_membership():
    # 先創建一個會員
    client.post("/membership", json={
        "pid": "P001",
        "acctname": "member_user",
        "acctpw": "securepassword",
        "email": "user@example.com"
    })
    # 更新會員信息
    payload = {
        "acctname": "updated_user",
        "acctpw": "newsecurepassword",
        "email": "updated_user@example.com"
    }
    response = client.put("/membership/P001", json=payload)
    print(response.status_code, response.json())  # 調試輸出
    assert response.status_code == 200
    assert response.json().get("acctname") == "updated_user"

# test delete membership
def test_delete_membership():
    # 先創建一個會員
    client.post("/membership", json={
        "pid": "P001",
        "acctname": "member_user",
        "acctpw": "securepassword",
        "email": "user@example.com"
    })
    # 刪除會員
    response = client.delete("/membership/P001")
    print(response.status_code, response.json())  # 調試輸出
    assert response.status_code == 200
    assert response.json().get("pid") == "P001"

# test get membership by pid
def test_get_membership_by_id():
    response = client.get("/membership/P001")
    print(response.status_code, response.json())  # 調試輸出
    assert response.status_code == 404
    assert response.json().get("detail") == "Not Found"

# test get all memberships
def test_get_all_memberships():
    # Create a new membership to test listing
    payload = {
        "pid": "P002",
        "acctname": "member_user_2",
        "acctpw": "anothersecurepassword",
        "email": "user2@example.com"
    }
    client.post("/membership", json=payload)
    response = client.get("/membership")
    print(response.status_code, response.json())  # 調試輸出
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# test create membership with missing fields
def test_create_membership_missing_fields():
    payload = {
        "acctname": "incomplete_user"
    }
    response = client.post("/membership", json=payload)
    print(response.status_code, response.json())  # 調試輸出
    assert response.status_code == 422

# test update non-existent membership
def test_update_non_existent_membership():
    payload = {
        "acctname": "non_existent_user",
        "acctpw": "nopassword",
        "email": "nonexistent@example.com"
    }
    response = client.put("/membership/P999", json=payload)
    print(response.status_code, response.json())  # 調試輸出
    assert response.status_code == 404
    assert response.json().get("detail") == "Not Found"

# test delete non-existent membership
def test_delete_non_existent_membership():
    response = client.delete("/membership/P999")
    print(response.status_code, response.json())  # 調試輸出
    assert response.status_code == 404
    assert response.json().get("detail") == "Not Found"
