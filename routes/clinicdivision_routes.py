from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.clinicdivision_service import create_clinic_division ,enable_clinic_division ,disable_clinic_division ,delete_clinic_division
from utils.db import get_db
from schemas.clinicdivision import ClinicDivisionCreate ,ClinicDivisionUpdate

clinicdivision_router = APIRouter()

@clinicdivision_router.post("/clinicdivision/create", status_code=201)
def create_clinic_division_endpoint(clinic_division: ClinicDivisionCreate, db: Session = Depends(get_db)):
    result = create_clinic_division(db=db, clinic_division_data=clinic_division)
    return result

@clinicdivision_router.put("/clinicdivision/enable", status_code=200)
def enable_clinic_division_endpoint(clinic_division: ClinicDivisionUpdate, db: Session = Depends(get_db)):
    result = enable_clinic_division(db=db, clinic_division_data=clinic_division)
    return result

@clinicdivision_router.put("/clinicdivision/disable", status_code=200)
def disable_clinic_division_endpoint(clinic_division: ClinicDivisionUpdate, db: Session = Depends(get_db)):
    result = disable_clinic_division(db=db, clinic_division_data=clinic_division)
    return result

@clinicdivision_router.delete("/clinicdivision/delete", status_code=200)
def delete_clinic_division_endpoint(clinic_division: ClinicDivisionUpdate, db: Session = Depends(get_db)):
    result = delete_clinic_division(db=db, clinic_division_data=clinic_division)
    return result
