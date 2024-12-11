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
from models import Clinic, Division ,Clinicdivision

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

def get_existings():
    with SessionLocal() as db:
        return {
            (division.divid, division.cid)
            for division in db.query(Clinicdivision).all()
        }

def generate_payload(divids ,cids ,existings):

    while True:
        divid = random.choice(divids)
        cid = random.choice(cids)
        if (divid ,cid) not in existings:
            existings.add((divid, cid))
            break
    return {
        "divid": divid,
        "cid": cid,
    }

def get_ids():

    with SessionLocal() as db:
        divids = [division.divid for division in db.query(Division).all()]
        cids = [clinic.cid for clinic in db.query(Clinic).all()]
        
    return divids, cids

def test_create_rooms():

    count = 5000
    divids ,cids = get_ids()
    existings = get_existings()

    if not (cids and divids):
        raise ValueError("資料庫中沒有可用的 Clinics 資料，無法生成 ClinicDivision 資料！")

    created_count = 0
    for _ in range(count):
        payload = generate_payload(divids ,cids ,existings)
        response = client.post("/clinicdivision/create", json=payload)
        print(f"Payload: {payload}")
        print(f"Response: {response.status_code} - {response.json()}")

        assert response.status_code == 201, f"Failed at payload: {payload}"
        created_count += 1

    print(f"成功新增 {created_count} 筆 ClinicDivision 資料！")