from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from services.clinic_service import create_clinic, update_clinic, delete_clinic, get_clinic_by_id, get_clinic_by_acct_name
from utils.db import get_db
from schemas.clinic import ClinicCreate, ClinicAuth, ClinicUpdate
import utils.security as sec

clinic_router = APIRouter()

@clinic_router.post("/clinics", status_code=201)
def create_clinic_endpoint(clinic: ClinicCreate, db: Session = Depends(get_db)):
    # hash the password
    clinic.acct_pw = sec.hash_password(clinic.acct_pw)
    result = create_clinic(db=db, clinic_data=clinic)
    return result  # 返回来自 service 层的消息和诊所 id

# update clinic
@clinic_router.put("/clinics/{cid}")
def update_clinic_endpoint(cid: str, clinic: ClinicUpdate, db: Session = Depends(get_db)):
    if clinic.acct_pw:
        clinic.acct_pw = sec.hash_password(clinic.acct_pw)
    result = update_clinic(db=db, cid=cid, clinic_update=clinic)
    if not result:
        raise HTTPException(status_code=404, detail="Clinic not found")

    return {"message": "Clinic updated successfully", "clinic": result.cid}

# delete clinic
@clinic_router.delete("/clinics/{cid}")
def delete_clinic_endpoint(cid: str, db: Session = Depends(get_db)):
    result = delete_clinic(db=db, cid=cid)
    if not result:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return {"message": "Clinic deleted successfully", "clinic": result.cid}

# get clinic by id
@clinic_router.get("/clinics/{cid}")
def get_clinic_by_id_endpoint(cid: str, db: Session = Depends(get_db)):
    result = get_clinic_by_id(db=db, cid=cid)
    if not result:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return result

# authenticate clinic
@clinic_router.post("/clinics/authenticate")
def authenticate_clinic_endpoint(auth: ClinicAuth, request: Request, db: Session = Depends(get_db)):
    # get clinic password hash
    acct_name = auth.acct_name
    password = auth.password
    clinic = get_clinic_by_acct_name(db=db, acct_name=acct_name)
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    # check password
    if not sec.verify_password(password, clinic.acct_pw):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        # 将用户信息存入会话

    session = request.session
    session['user_id'] = clinic.cid
    session['welcome_state'] = True
    session['manage_state'] = False
    session['appointment_state'] = False
    return {"message": "Clinic authenticated successfully", "clinic": clinic.cid}