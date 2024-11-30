from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.clinic_service import create_clinic
from utils.db import get_db
from schemas.clinic import ClinicCreate

clinic_router = APIRouter()

@clinic_router.post("/clinics", status_code=201)
def create_clinic_endpoint(clinic: ClinicCreate, db: Session = Depends(get_db)):
    result = create_clinic(db=db, clinic_data=clinic)
    return result  # 返回来自 service 层的消息和诊所 id
