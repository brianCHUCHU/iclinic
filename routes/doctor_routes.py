from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.doctor import Doctor
from services.doctor_service import create_doctor ,update_doctor_name
from utils.db import get_db
from schemas.doctor import DoctorCreate ,DoctorUpdate

doctor_router = APIRouter()

@doctor_router.post("/doctor", status_code=201)
def create_doctor_endpoint(doctor: DoctorCreate, db: Session = Depends(get_db)):
    result = create_doctor(db=db, doctor_data=doctor)
    return result

@doctor_router.put("/doctor", status_code=200)
def update_doctor_name_endpoint(doctor: DoctorUpdate, db: Session = Depends(get_db)):
    result = update_doctor_name(db=db, docid=doctor.docid, new_name=doctor)  # 調用 update_doctor_name
    return result

    return {"message": "Doctor name updated successfully", "doctor": doctor_to_update}
