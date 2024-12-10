# from fastapi.testclient import TestClient
# from main import app
# from sqlalchemy.orm import Session
# from utils.db import SessionLocal
# from models import Clinic, Division
# from faker import Faker
# from contextlib import contextmanager
# import random
# import pytest
# from utils.id_check import id_generator

# ##pytest.skip(allow_module_level=True)

# @contextmanager
# def get_db_session():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# client = TestClient(app)
# fake = Faker()

# def get_existing_cids_and_divids():

#     with SessionLocal() as db:
#         cids = [clinic.cid for clinic in db.query(Clinic).all()]
#         divids = [division.divid for division in db.query(Division).all()]
#     return cids, divids


# def generate_hire_payload(cids, divids):

#     payload = {
#         "docid": id_generator(),
#         "docname": fake.name(),  # 使用 Faker 生成名字
#         "cid": random.choice(cids),
#         "divid": random.choice(divids),
#         "startdate": f"{random.randint(2000, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
#     }
#     return payload


# def test_create_hires():

#     count = 50  # 設定要生成的 hire 數量
#     cids, divids = get_existing_cids_and_divids()

#     if not cids or not divids:
#         raise ValueError("資料庫中沒有可用的 Clinic 或 Division 資料，無法生成 hire！")

#     created_count = 0
#     for _ in range(count):
#         payload = generate_hire_payload(cids, divids)
#         response = client.post("/hire", json=payload)
#         assert response.status_code == 201, f"Failed at payload: {payload}"
#         assert response.json().get("message") == "Hire created successfully"
#         print(f"成功新增 Hire: {payload['docname']} (cid: {payload['cid']}, divid: {payload['divid']})")
#         created_count += 1

#     print(f"成功新增 {created_count} 筆 hire 資料！")
