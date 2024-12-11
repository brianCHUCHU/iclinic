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

def generate_payload(date):
    with SessionLocal() as db:
        appointments = db.query(Appointment).filter(Appointment.date == date).all()
        if appointments:
            return appointments
        else:
            return "No appointments found for the given date."


def test_create_appointment():

    count = 500
    ##date = fake.date_between(start_date="today", end_date="+20day")
    date = "2024-12-19"

    for _ in range(count):
        results = generate_payload(date)

        if results != "No appointments found for the given date.":
            for appointment in results:
                ans =(f"PID: {appointment.pid}, SID: {appointment.sid}, Date: {appointment.date}")
        else:
            print(results)
