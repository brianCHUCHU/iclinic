from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from utils.db import SessionLocal
from faker import Faker
from contextlib import contextmanager
import random
import pytest
from utils.id_check import id_generator
import string
from models import Clinic

pytest.skip(allow_module_level=True)

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

    rid = "R" + "".join(random.choices(string.digits, k=9))
    cid = random.choice(cids)
    rname = f"{random.randint(00000, 99999):05d}"


    return {
        "rid": rid,
        "cid": cid,
        "rname": rname
    }

def get_existing_cids():

    with SessionLocal() as db:
        cids = [clinic.cid for clinic in db.query(Clinic).all()]
    return cids

def test_create_rooms():

    count = 5000
    cids = get_existing_cids()

    if not cids:
        raise ValueError("資料庫中沒有可用的 Clinics 資料，無法生成 Room 資料！")

    created_count = 0
    for _ in range(count):
        payload = generate_payload(cids)
        response = client.post("/room", json=payload)
        print(f"Payload: {payload}")
        print(f"Response: {response.status_code} - {response.json()}")

        assert response.status_code == 201, f"Failed at payload: {payload}"
        created_count += 1

    print(f"成功新增 {created_count} 筆 Room 資料！")