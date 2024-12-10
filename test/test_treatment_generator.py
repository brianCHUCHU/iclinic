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
from models import Division ,Clinic ,Doctor

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

def generate_period_payload(docids ,divids ,cids):

    tid = f"{random.randint(0, 9999999999):010d}"
    docid = random.choice(docids)
    divid =random.choice(divids)
    cid =random.choice(cids)
    tname = f"{random.randint(0, 9999999999):010d}"

    return {
        "tid": tid,
        "docid": docid,
        "divid": divid,
        "cid": cid,
        "tname": tname
    }

# def get_existing_ids():
#     with SessionLocal() as db:
#         docname =[doctor.docname for doctor in db.query(Doctor).all()]
#         divname =[division.divname for division in db.query(Division).all()]
#         return docname ,divname

def get_existing_ids():

    with SessionLocal() as db:
        docids = [doctor.docid for doctor in db.query(Doctor).all()]
        divids = [division.divid for division in db.query(Division).all()]
        cids = [clinic.cid for clinic in db.query(Clinic).all()]
    return docids, divids ,cids

def test_create_periods():

    count = 50
    docids ,divids ,cids = get_existing_ids()

    if not (docids and divids and cids):
        raise ValueError("資料庫中沒有可用的資料，無法生成 Treatment 資料！")

    created_count = 0
    for _ in range(count):
        payload = generate_period_payload(docids ,divids ,cids)
        response = client.post("/treatment", json=payload)
        print(f"Payload: {payload}")
        print(f"Response: {response.status_code} - {response.json()}")

        assert response.status_code == 201, f"Failed at payload: {payload}"
        created_count += 1

    print(f"成功新增 {created_count} 筆 Treatment 資料！")