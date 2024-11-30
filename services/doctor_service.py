from sqlalchemy.orm import Session
from models.doctor import Doctor
from schemas.doctor import DoctorCreate ,DoctorUpdate
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
