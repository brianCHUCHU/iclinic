from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.clinic_service import create_clinic, update_clinic, delete_clinic, get_clinic_by_id
from utils.db import get_db
from schemas.clinic import ClinicCreate

clinic_router = APIRouter()

@clinic_router.post("/clinics", status_code=201)
def create_clinic_endpoint(clinic: ClinicCreate, db: Session = Depends(get_db)):
    result = create_clinic(db=db, clinic_data=clinic)
    return result  # 返回来自 service 层的消息和诊所 id

# update clinic
@clinic_router.put("/clinics/{cid}")
def update_clinic_endpoint(cid: str, clinic: ClinicCreate, db: Session = Depends(get_db)):
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