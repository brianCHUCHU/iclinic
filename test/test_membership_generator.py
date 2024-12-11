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
from models import Patient, Membership
import csv
import os

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

def generate_payload(pids):

    while True:
        pid = id_generator()
        if pid not in pids:
            break
    acct_pw = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    with SessionLocal() as db:
        while True:
            email = f"user_{random.randint(0, 9999999999):010d}@example.com"
            if email not in set(email[0] for email in db.query(Membership.email).all()):
                break
    pname = fake.name()
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=100)
    gender = fake.random_element(elements=["M", "F"])

    csv_file = "./pw/membership_accounts.csv"
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["pid", "acct_pw"])
        writer.writerow([pid, acct_pw])

    return {
        "pid": pid,
        "acct_pw": acct_pw,
        "email": email,
        "pname": pname,
        "birthdate": birthdate.isoformat(),
        "gender": gender
    }

def get_existing_ids():

    with SessionLocal() as db:
        pids = [patient.pid for patient in db.query(Patient).all()]
    if not pids:
        return None
    return pids

def test_create_memberships():

    count = 500
    pids = get_existing_ids()

    created_count = 0
    for _ in range(count):
        payload = generate_payload(pids)
        response = client.post("/memberships", json=payload)
        print(f"Payload: {payload}")
        print(f"Response: {response.status_code} - {response.json()}")

        assert response.status_code == 201, f"Failed at payload: {payload}"
        created_count += 1

    print(f"成功新增 {created_count} 筆 Membership 資料！")

