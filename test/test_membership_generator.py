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
from models import Patient

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

def generate_payload(pids):

    existing_pids = []
    while True:
        pid = random.choice(pids ,existing_pids)
        if pid not in existing_pids:  # 確保 pid 唯一
            existing_pids.append(pid)
            break
    acctpw: str ="".join(random.choices(string.ascii_letters + string.digits, k=10))
    email = f"user_{random.randint(1000, 9999)}@example.com"

    return {
        "pid": pid,
        "acctpw": acctpw,
        "email": email
    }


def get_existing_ids():

    with SessionLocal() as db:
        pids = [patient.pid for patient in db.query(Patient).all()]
    return pids

def test_create_memberships():

    count = 50
    pids = get_existing_ids()

    if not pids:
        raise ValueError("資料庫中沒有可用的資料，無法生成 Treatment 資料！")

    created_count = 0
    for _ in range(count):
        payload = generate_payload(pids)
        response = client.post("/memberships", json=payload)
        print(f"Payload: {payload}")
        print(f"Response: {response.status_code} - {response.json()}")

        assert response.status_code == 201, f"Failed at payload: {payload}"
        created_count += 1

    print(f"成功新增 {created_count} 筆 Membership 資料！")