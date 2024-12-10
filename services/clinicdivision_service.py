from sqlalchemy.orm import Session
from models import Clinicdivision
from schemas.clinicdivision import ClinicDivisionCreate, ClinicDivisionUpdate
from fastapi import HTTPException


def create_clinic_division(db: Session, clinic_division_data: ClinicDivisionCreate):
    existing_clinic_division = db.query(Clinicdivision).filter_by(divid=clinic_division_data.divid, cid=clinic_division_data.cid).first()
    if existing_clinic_division:
        raise HTTPException(status_code=400, detail="Clinic division already exists")
    clinic_division_dict = clinic_division_data.model_dump()
    new_clinic_division = Clinicdivision(**clinic_division_dict)

    db.add(new_clinic_division)
    db.commit()
    db.refresh(new_clinic_division)
    return {"message": "Clinic division created successfully", "clinic_division": new_clinic_division}

def enable_clinic_division(db: Session, clinic_division_data: ClinicDivisionUpdate):
    clinic_division = db.query(Clinicdivision).filter_by(divid=clinic_division_data.divid, cid=clinic_division_data.cid).first()
    if not clinic_division:
        raise HTTPException(status_code=404, detail="Clinic division not found")
    clinic_division.available = True
    db.commit()
    db.refresh(clinic_division)
    return {"message": "Clinic division enabled successfully", "clinic_division": clinic_division}

def disable_clinic_division(db: Session, clinic_division_data: ClinicDivisionUpdate):
    clinic_division = db.query(Clinicdivision).filter_by(divid=clinic_division_data.divid, cid=clinic_division_data.cid).first()
    if not clinic_division:
        raise HTTPException(status_code=404, detail="Clinic division not found")
    clinic_division.available = False
    db.commit()
    db.refresh(clinic_division)
    return {"message": "Clinic division disabled successfully", "clinic_division": clinic_division}

def delete_clinic_division(db: Session, clinic_division_data: ClinicDivisionUpdate):
    clinic_division = db.query(Clinicdivision).filter_by(divid=clinic_division_data.divid, cid=clinic_division_data.cid).first()
    if not clinic_division:
        raise HTTPException(status_code=404, detail="Clinic division not found")
    db.delete(clinic_division)
    db.commit()
    return {"message": "Clinic division deleted successfully"}