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

def generate_member(db: Session, count: int = 1):

    generated_pids = set()
    patients = []

    for _ in range(count):
        while True:
            pid = id_generator()
            if pid not in generated_pids:
                generated_pids.add(pid)
                break
        acctpw: str ="".join(random.choices(string.ascii_letters + string.digits, k=10))
        email = f"user_{random.randint(1000, 9999)}@example.com"

        patient_data = {
            "pid": pid,
            "acctpw": acctpw,
            "email": email
        }

        new_patient = Patient(**patient_data)
        patients.append(new_patient)

    db.add_all(patients)
    db.commit()
    return patients

def test_generate_member():
    count = 100
    with get_db_session() as db:
            patients = generate_member(db, count=count)
            assert len(patients) == count