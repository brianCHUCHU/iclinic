from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from utils.db import SessionLocal
from models import Clinic
from faker import Faker
from contextlib import contextmanager
import random
import pytest
from utils.id_check import id_generator
from datetime import time, timedelta
import string

##pytest.skip(allow_module_level=True)

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

fake = Faker()

client = TestClient(app)

def generate_payload(cids):

    perid: str = "P" + "".join(random.choices(string.digits, k=9))
    cid = random.choice(cids)
    weekday = str(random.randint(1, 7))
    start_hour = random.randint(6, 17) 
    start_minute = random.choice([0, 15, 30, 45])
    starttime = time(hour=start_hour, minute=start_minute)

    end_hour = random.randint(start_hour + 1, 23)
    end_minute = random.choice([0, 15, 30, 45])
    endtime = time(hour=end_hour, minute=end_minute)

    return {
        "perid": perid,
        "cid": cid,
        "weekday": weekday,
        "starttime": starttime.strftime("%H:%M"),
        "endtime": endtime.strftime("%H:%M")
    }

def get_existing_ids():

    with SessionLocal() as db:
        cids = [clinic.cid for clinic in db.query(Clinic).all()]
    return cids

def test_create_periods():

    count = 500  # 設定要生成的 Period 數量
    cids = get_existing_ids()  # 獲取有效的 Clinic Ids

    if not cids:
        raise ValueError("資料庫中沒有可用的 Clinics 資料，無法生成 Period 資料！")

    created_count = 0
    for _ in range(count):
        payload = generate_payload(cids)
        response = client.post("/period", json=payload)
        print(f"Payload: {payload}")
        print(f"Response: {response.status_code} - {response.json()}")

        assert response.status_code == 201, f"Failed at payload: {payload}"
        created_count += 1

    print(f"成功新增 {created_count} 筆 Period 資料！")
