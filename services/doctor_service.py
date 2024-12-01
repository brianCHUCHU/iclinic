from sqlalchemy.orm import Session
from models.doctor import Doctor, Hire
from schemas.doctor import DoctorCreate ,DoctorUpdate, HireCreate, HireUpdate
from fastapi import HTTPException
from passlib.context import CryptContext

def create_doctor(db: Session, doctor_data: DoctorCreate):
    existing_doctor = db.query(Doctor).filter_by(docid=doctor_data.docid).first()
    if existing_doctor:
        raise HTTPException(status_code=400, detail="Docotr already exists")

    new_doctor = Doctor(
        docid=doctor_data.docid,
        docname=doctor_data.docname,
    )
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return {"message": "Doctor created successfully","doctor":new_doctor}

def update_doctor_name(db: Session, docid: str, new_name: DoctorUpdate):
    doctor = db.query(Doctor).filter_by(docid=docid).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor.docname = new_name.docname
    db.commit()
    db.refresh(doctor)
    return {"message": "Doctor name updated successfully", "doctor": doctor}

def get_doctor(db: Session, docid: str = None, docname: str = None):
    if docid:
        return db.query(Doctor).filter(Doctor.docid == docid).first()
    elif docname:
        return db.query(Doctor).filter(Doctor.docname == docname).first()
    return None

def create_hire(db: Session, hire_data: HireCreate):
    existing_hire = db.query(Hire).filter_by(docid=hire_data.docid, cid=hire_data.cid, divid=hire_data.divid).first()
    if existing_hire:
        raise HTTPException(status_code=400, detail="Hire already exists")

    new_hire = Hire(
        docid=hire_data.docid,
        cid=hire_data.cid,
        divid=hire_data.divid,
        startdate=hire_data.startdate,
        enddate=hire_data.enddate
    )
    db.add(new_hire)
    db.commit()
    db.refresh(new_hire)
    return {"message": "Hire created successfully","hire":new_hire}

def update_hire(db: Session, docid: str, cid: str, divid: str, hire_update: HireUpdate):
    hire = db.query(Hire).filter_by(docid=docid, cid=cid, divid=divid).first()
    if not hire:
        raise HTTPException(status_code=404, detail="Hire not found")
    hire.startdate = hire_update.startdate
    hire.enddate = hire_update.enddate
    db.commit()
    db.refresh(hire)
    return {"message": "Hire updated successfully", "hire": hire}
