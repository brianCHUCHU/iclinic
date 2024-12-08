from sqlalchemy.orm import Session
from models.patient import Patient
from schemas.patient import PatientCreate, PatientUpdate
from fastapi import HTTPException
from utils.id_validation import id_check

# 新增病患
def create_patient(db: Session, patient_data: PatientCreate):
    if not id_check(patient_data.pid):
        raise HTTPException(status_code=400, detail="Invalid patient id")
    new_patient = Patient(**patient_data.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

# 查詢病患 (根據 PID 或其他條件)
def get_patient(db: Session, pid: str = None, pname: str = None):
    if pid and not id_check(pid):
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

def generate_patient(db: Session, pid: str):
    if not id_check(patient_data.pid):
        raise HTTPException(status_code=400, detail="Invalid patient id")
    new_patient = Patient(**patient_data.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient
    