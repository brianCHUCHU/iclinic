from sqlalchemy.orm import Session
from models import Doctor, Hire
from models import Clinic
from models import Division
from schemas.doctor import DoctorCreate ,DoctorUpdate, HireCreate, HireUpdate, DoctorAndHireCreate
from fastapi import HTTPException
from utils.id_check import id_validator

def create_doctor(db: Session, doctor_data: DoctorCreate):
    if not id_validator(doctor_data.docid):
        raise HTTPException(status_code=400, detail="Invalid doctor id")
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
    if docid and not id_validator(docid):
        raise HTTPException(status_code=400, detail="Invalid doctor id")
    if docid:
        return db.query(Doctor).filter(Doctor.docid == docid).first()
    elif docname:
        return db.query(Doctor).filter(Doctor.docname == docname).all()
    return None

def create_hire(db: Session, hire_data: HireCreate):
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

def get_hire(db: Session, docid: str = None, cid: str = None, divid: str = None, docname: str = None):
    if docid and not id_validator(docid):
        raise HTTPException(status_code=400, detail="Invalid doctor id")
    query = db.query(Hire).filter(Hire.enddate == None)

    # 可選條件動態加入
    if docid:
        query = query.filter(Hire.docid == docid)
    if cid:
        query = query.filter(Hire.cid == cid)
    if divid:
        query = query.filter(Hire.divid == divid)

    # 加入外部連結
    query = query.join(Doctor, Hire.docid == Doctor.docid, isouter=True)
    if docname:
        query = query.filter(Doctor.docname == docname)
    
    query = query.join(Clinic, Hire.cid == Clinic.cid, isouter=True)
    query = query.join(Division, Hire.divid == Division.divid, isouter=True)
    query = query.with_entities(Hire, Doctor.docname, Clinic.cname, Division.divname)

    # 判斷返回多筆或單筆
    if docid or (cid and divid and docname):
        return query.first()  # 返回單筆資料
    return query.all()  # 返回多筆資料

# create doctor if doctor not exists, then create hire, if hire exists, update hire
def create_or_update_hire(db: Session, data: DoctorAndHireCreate):
    if not id_validator(data.docid):
        raise HTTPException(status_code=400, detail="Invalid doctor id")
    # Step 1: Ensure the doctor exists using get_doctor
    doctor = get_doctor(db, docid=data.docid)
    if not doctor:
        if not data.docname:
            raise HTTPException(status_code=400, detail="Doctor name is required")
        result = create_doctor(db, DoctorCreate(docid=data.docid, docname=data.docname))

    # Step 2: try update hire if hire exists
    try:
        return update_hire(db, docid=data.docid, cid=data.cid, divid=data.divid, hire_update=HireUpdate(startdate=data.startdate, enddate=data.enddate))
    except HTTPException:
        pass

    # Step 3: Create a new hire
    return create_hire(db, HireCreate(docid=data.docid, cid=data.cid, divid=data.divid, startdate=data.startdate, enddate=data.enddate))