from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from utils.db import SessionLocal
from models import Patient, Schedule, Appointment
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

    while True:
        pid = random.choice(pids)
        sid = random.choice(sids)
        if (pid ,sid) not in existings:
            existings.add((pid ,sid))
            break
    return pid ,sid

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
        print(f"PIDs: {pids}")
        print(f"SIDs: {sids}")
    return pids ,sids

def test_create_appointment():

    count = 500000
    pids ,sids = get_ids()
    existings = get_existings()

    created_count = 0
    for _ in range(count):
        ans =generate_payload(pids ,sids ,existings)
