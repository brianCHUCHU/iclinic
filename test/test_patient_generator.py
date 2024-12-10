from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from main import app
from faker import Faker
from models import Patient
from utils.id_check import id_generator
from fastapi import APIRouter
from contextlib import contextmanager
from utils.db import SessionLocal
import pytest

pytest.skip(allow_module_level=True)

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




client = TestClient(app)
fake = Faker()

def generate_patient(db: Session, count: int = 1):

    generated_pids = set()
    patients = []

    for _ in range(count):
        while True:
            pid = id_generator()
            if pid not in generated_pids:
                generated_pids.add(pid)
                break

        patient_data = {
            "pid": pid,
            "pname": fake.name(),
            "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=100),
            "gender": fake.random_element(elements=["M", "F"]),
            "status" : "G"
        }

        new_patient = Patient(**patient_data)
        patients.append(new_patient)

    db.add_all(patients)
    db.commit()
    return patients

def test_generate_patient():
    count = 100
    with get_db_session() as db:
            patients = generate_patient(db, count=count)
            assert len(patients) == count

