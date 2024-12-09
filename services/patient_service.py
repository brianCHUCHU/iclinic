from sqlalchemy.orm import Session
from models import Patient
from schemas.patient import PatientCreate, PatientUpdate
from fastapi import HTTPException
from utils.id_check import id_validator
from faker import Faker
import random
import string
import re

# 新增病患
def create_patient(db: Session, patient_data: PatientCreate):
    if not id_validator(patient_data.pid):
        raise HTTPException(status_code=400, detail="Invalid patient id")
    new_patient = Patient(**patient_data.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

# 查詢病患 (根據 PID 或其他條件)
def get_patient(db: Session, pid: str = None, pname: str = None):
    if pid and not id_validator(pid):
        raise HTTPException(status_code=400, detail="Invalid patient id")
    if pid:
        return db.query(Patient).filter(Patient.pid == pid).first()
    if pname:
        return db.query(Patient).filter(Patient.pname == pname).all()
    raise HTTPException(status_code=400, detail="Invalid query parameters")

# 更新病患資料
def update_patient(db: Session, pid: str, patient_update: PatientUpdate):
    patient = get_patient(db, pid=pid)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in patient_update.model_dump(exclude_unset=True).items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return patient

# 刪除病患
def delete_patient(db: Session, pid: str):
    patient = get_patient(db, pid=pid)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return patient

fake = Faker()
def regexify() -> str:
    first_char = random.choice(string.ascii_uppercase)
    rest_chars = ''.join(random.choices(string.digits, k=9))
    return first_char + rest_chars

'''
def generate_patient(db: Session ,count : int = 1):
    generated_pids = set()
    patients = []

    while len(patients) < count:
        pid = regexify(r'[A-Z0-9]{10}')
        if pid in generated_pids:
            continue

        generated_pids.add(pid)
    
        patient_data = {
            "pid": pid,
            "pname": fake.name(),
            "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=100),
            "gender": fake.random_element(elements=["M", "F"]),
            "status" : "G"
        }

    # 創建新的病患
        new_patient = Patient(**patient_data)
        patients.append(new_patient)
    db.add_all(patients)
    db.commit()
    return patients
'''