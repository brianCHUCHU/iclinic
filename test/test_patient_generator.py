from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from main import app
from faker import Faker
from models import Patient
from utils.db import get_db
from models import Base
from utils.id_check import id_generator
import pytest

pytest.skip(allow_module_level=True)

client = TestClient(app)
fake = Faker()

def generate_patients(db: Session, count: int = 1):

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
            "pname": fake.first_name()[:100],
            "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=100),
            "gender": fake.random_element(elements=["M", "F"]),
            "status": fake.random_element(elements=["A", "I", "G"])
        }

        new_patient = Patient(**patient_data)
        patients.append(new_patient)

    db.add_all(patients)
    db.commit()
    return patients

def test_generate_patients():

    count = 500
    response = client.post(f"/patients/generate?count={count}")
    
    assert response.status_code == 201
    data = response.json()

    assert data["message"] == f"{count} patients generated successfully"
    assert len(data["patients"]) == count


