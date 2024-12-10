# from fastapi.testclient import TestClient
# from main import app
# from sqlalchemy.orm import Session
# from utils.db import SessionLocal
# from faker import Faker
# from contextlib import contextmanager
# import random
# import pytest
# from utils.id_check import id_generator
# import string
# from models import Division ,Period ,Doctor

# ##pytest.skip(allow_module_level=True)

# @contextmanager
# def get_db_session():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# fake = Faker()

# client = TestClient(app)

# def generate_payload(divids ,perids ,docids):

#     sid = f"{random.randint(0, 9999999999):010d}"
#     divid = random.choice(divids)
#     perid =random.choice(perids)
#     docid =random.choice(docids)

#     return {
#         "sid": sid,
#         "divid": divid,
#         "perid": perid,
#         "docid": docid
#     }

# def get_existing_ids():

#     with SessionLocal() as db:
#         divids = [division.divid for division in db.query(Division).all()]
#         perids = [period.perid for period in db.query(Period).all()]
#         docids = [doctor.docid for doctor in db.query(Doctor).all()]
#     return divids ,perids ,docids

# def test_create_schedules():

#     count = 50
#     divids ,perids ,docids = get_existing_ids()

#     if not (divids and perids and docids):
#         raise ValueError("資料庫中沒有可用的資料，無法生成 Schedule 資料！")

#     created_count = 0
#     for _ in range(count):
#         payload = generate_payload(divids ,perids ,docids)
#         response = client.post("/schedule", json=payload)
#         print(f"Payload: {payload}")
#         print(f"Response: {response.status_code} - {response.json()}")

#         assert response.status_code == 201, f"Failed at payload: {payload}"
#         created_count += 1

#     print(f"成功新增 {created_count} 筆 Schedule 資料！")