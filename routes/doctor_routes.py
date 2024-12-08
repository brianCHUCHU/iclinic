from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Doctor
from services.doctor_service import create_doctor ,update_doctor_name, get_hire, create_or_update_hire
from utils.db import get_db
from schemas.doctor import DoctorCreate ,DoctorUpdate, HireCreate, HireUpdate, DoctorAndHireCreate

doctor_router = APIRouter()

@doctor_router.post("/doctor", status_code=201)
def create_doctor_endpoint(doctor: DoctorCreate, db: Session = Depends(get_db)):
    result = create_doctor(db=db, doctor_data=doctor)
    return result

@doctor_router.put("/doctor", status_code=200)
def update_doctor_name_endpoint(doctor: DoctorUpdate, db: Session = Depends(get_db)):
    result = update_doctor_name(db=db, docid=doctor.docid, new_name=doctor)  # 調用 update_doctor_name
    return result

@doctor_router.get("/hire")
def get_hire(db: Session = Depends(get_db), docid: str = None, cid: str = None, divid: str = None, docname: str = None):
    result = get_hire(db=db, docid=docid, cid=cid, divid=divid)
    return result

@doctor_router.post("/hire", status_code=201)
def create_or_update_hire_endpoint(hire: DoctorAndHireCreate, db: Session = Depends(get_db)):
    result = create_or_update_hire(db=db, data=hire)
    return result