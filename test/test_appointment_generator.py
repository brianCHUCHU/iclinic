from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from utils.db import SessionLocal
from models import Patient, Schedule, Appointment, Period
from faker import Faker
from contextlib import contextmanager
import random
import pytest
from utils.id_check import id_generator
from datetime import time, timedelta
import string
from sqlalchemy import func
from datetime import datetime

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

def generate_payload(pids ,sids ,existings):

    with SessionLocal() as db:
        while True:
            pid = random.choice(pids)
            sid = random.choice(sids)
            if (pid ,sid) not in existings:
                existings.add((pid ,sid))
                break
        perid_row = db.query(Schedule.perid).filter(Schedule.sid == sid).first()
        if perid_row:
            perid = perid_row[0]
        weekday_row = db.query(Period.weekday).filter(Schedule.perid == perid).first()
        if weekday_row:
            weekday = weekday_row[0]
        weekday = weekday-1
        while True:
            date = fake.date_between(start_date="today", end_date="+20days")
            if date.weekday() == weekday:
                break
        order = get_latest(sid, date)+1
        applytime = datetime.now()
        status = random.choice(['P', 'O'])
        return {
            "pid": pid,
            "sid": sid,
            "date": date.isoformat(),
            "order" : order,
            "applytime" : applytime.isoformat(),
            "status" : status
        }

def get_existings():
    with SessionLocal() as db:
        return {
            (appointment.pid, appointment.sid)
            for appointment in db.query(Appointment).all()
        }
    
def get_latest(sid, date):
    with SessionLocal() as db:
        # 查詢符合指定 sid 和 date 的最大 order
        return (
            db.query(func.max(Appointment.order))
            .filter(Appointment.sid == sid, Appointment.date == date)
            .scalar()
            or 0  # 如果查詢結果為 None，返回 0
        )

def get_ids():

    with SessionLocal() as db:
        pids = [patient.pid for patient in db.query(Patient).all()]
        sids = [schedule.sid for schedule in db.query(Schedule).all()]
        print(f"PIDs: {pids}")
        print(f"SIDs: {sids}")
    return pids ,sids

def test_create_appointment():

    count = 1000
    pids ,sids = get_ids()
    existings = get_existings()

    if not (pids and sids):
        raise ValueError("資料庫中沒有可用的資料，無法生成 Appointment 資料！")

    created_count = 0
    for _ in range(count):
        payload = generate_payload(pids ,sids ,existings )
        response = client.post("/appointment", json=payload)
        print(f"Payload: {payload}")
        print(f"Response: {response.status_code} - {response.json()}")

        assert response.status_code == 201, f"Failed at payload: {payload}"
        created_count += 1

    print(f"成功新增 {created_count} 筆 ClinicDivision 資料！")