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
from models import Period ,Doctor ,Hire, Schedule

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

def generate_payload(docids):
    tried_docids = set()
    with SessionLocal() as db:
        while True:
            if len(tried_docids) >= len(docids):
                break
            docid = random.choice(docids)
            if docid in tried_docids:
                continue
            tried_docids.add(docid)
            duals = [
                (hire.divid, hire.cid)
                for hire in db.query(Hire).filter(Hire.docid == docid).all()
            ]
            divid, cid = random.choice(duals)
            if not (divid and cid):
                continue
            perids = [ period.perid for period in db.query(Period).filter(Period.cid == cid).all()]
            if not perids:
                continue
            perid = random.choice(perids)
            if not perid:
                continue
            sid : str = "S" + "".join(random.choices(string.digits, k=9))
            existing_schedule = db.query(Schedule).filter(
                Schedule.docid == docid, Schedule.perid == perid, Schedule.divid == divid
            ).first()
            if not existing_schedule:
                break
        return {
            "sid": sid,
            "divid": divid,
            "perid": perid,
            "docid": docid
        }   

def get_ids():

    with SessionLocal() as db:
        docids = [doctor.docid for doctor in db.query(Doctor).all()]
    return docids

def test_create_schedules():

    count = 500
    docids = get_ids()

    if not docids:
        raise ValueError("資料庫中沒有可用的資料，無法生成 Schedule 資料！")

    created_count = 0
    for _ in range(count):
        payload = generate_payload(docids)
        response = client.post("/schedule", json=payload)
        print(f"Payload: {payload}")
        print(f"Response: {response.status_code} - {response.json()}")

        assert response.status_code == 201, f"Failed at payload: {payload}"
        created_count += 1

    print(f"成功新增 {created_count} 筆 Schedule 資料！")