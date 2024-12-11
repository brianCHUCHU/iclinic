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
import os
import csv

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
        
        return pid ,sid ,date

def get_existings():
    with SessionLocal() as db:
        return {
            (appointment.pid, appointment.sid)
            for appointment in db.query(Appointment).all()
        }

def get_ids():

    with SessionLocal() as db:
        pids = [patient.pid for patient in db.query(Patient).all()]
        sids = [schedule.sid for schedule in db.query(Schedule).all()]
    return pids ,sids

def test_create_rooms():

    count = 5000
    pids ,sids = get_ids()
    existings = get_existings()
    
    created_count = 0
    for _ in range(count):
        pid ,sid ,date = generate_payload(pids ,sids ,existings)
        csv_file = "./src/appointment.csv"
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:  # 如果檔案不存在，寫入標題行
                writer.writerow(["pid" ,"sid" ,"date"])
            writer.writerow([pid ,sid ,date])  # 追加內容
        created_count += 1
