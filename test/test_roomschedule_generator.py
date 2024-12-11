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
from models import Schedule, Period, Room, Roomschedule

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

def generate_payload(sids):
    tried_sids = set()
    with SessionLocal() as db:
        while True:
            if len(tried_sids) >= len(sids):
                break
            sid = random.choice(sids)
            if sid in tried_sids:
                continue
            tried_sids.add(sid)
            perid = db.query(Schedule.perid).filter(Schedule.sid == sid).scalar()
            if not perid:
                continue
            cid = db.query(Period.cid).filter(Period.perid == perid).scalar()
            if not cid:
                continue
            rids = [
                room.rid
                for room in db.query(Room).filter(Room.cid.in_([cid])).all()
            ]
            if rids:
                rid = random.choice(rids)
                existing_schedule = db.query(Roomschedule).filter(
                    Roomschedule.sid == sid, Roomschedule.rid == rid, Roomschedule.cid == cid
                ).first()
                if existing_schedule:
                    continue
            elif not rids:
                continue
            return {
                "sid": sid,
                "rid": rid,
                "cid": cid,
            }

def get_ids():

    with SessionLocal() as db:
        sids = [schedule.sid for schedule in db.query(Schedule).all()]
        
    return sids

def test_roomschedule_generator():

    count = 500
    sids = get_ids()

    if not sids:
        raise ValueError("資料庫中沒有可用的資料，無法生成 RoomSchedule 資料！")

    created_count = 0
    for _ in range(count):
        payload = generate_payload(sids)
        if payload is None:
            break
        response = client.post("/roomschedule/create", json=payload)
        print(f"Payload: {payload}")
        print(f"Response: {response.status_code} - {response.json()}")

        assert response.status_code == 201, f"Failed at payload: {payload}"
        created_count += 1

    print(f"成功新增 {created_count} 筆 RoomSchedule 資料！")