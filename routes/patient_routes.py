from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.patient_service import create_patient, get_patient, update_patient, delete_patient
from utils.db import get_db
from schemas.patient import PatientCreate, PatientUpdate

patient_router = APIRouter()

@patient_router.post("/patients", status_code=201)
def create_patient_endpoint(patient: PatientCreate, db: Session = Depends(get_db)):
    result = create_patient(db=db, patient_data=patient)
    return {"message": "Patient created successfully", "patient": result}

@patient_router.get("/patients")
def get_patient_endpoint(db: Session = Depends(get_db), pid: str = None, pname: str = None):
    if pid:
        patient = get_patient(db=db, pid=pid)
    elif pname:
        patient = get_patient(db=db, pname=pname)
    else:
        raise HTTPException(status_code=400, detail="Invalid query parameters")
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"patient": patient}

@patient_router.put("/patients/{pid}", status_code=200)
def update_patient_endpoint(pid: str, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    updated_patient = update_patient(db=db, pid=pid, patient_update=patient_update)
    return {"message": "Patient updated successfully", "patient": updated_patient}

@patient_router.delete("/patients/{pid}", status_code=200)
def delete_patient_endpoint(pid: str, db: Session = Depends(get_db)):
    deleted_patient = delete_patient(db=db, pid=pid)
    return {"message": "Patient deleted successfully", "patient": deleted_patient}
