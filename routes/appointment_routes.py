from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.appointment import Appointment
from services.appointment_service import create_appointment ,update_appointment ,get_appointment
from utils.db import get_db
from schemas.appointment import AppointmentCreate ,AppointmentUpdate

appointment_router = APIRouter()

@appointment_router.post("/appointment", status_code=201)
def create_appointment_endpoint(appointment: AppointmentCreate ,db: Session = Depends(get_db)):
    result = create_appointment(db= db ,appointment_data= appointment)
    return result

@appointment_router.put("/appointment", status_code=200)
def update_appointment_endpoint(appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    result = update_appointment(db=db, pid=appointment.pid, new=appointment)
    return result

@appointment_router.get("/appointment")
def get_appointment_endpoint(
    db: Session = Depends(get_db),
    pid: str = None, 
    sid: str = None, 
    date : str = None , 
    order : str = None , 
    applytime: str = None,
    status : str = None,
    attendence : str = None
):
    if not any([pid, sid, date, order, applytime ,status, attendence]):
        raise HTTPException(status_code=400, detail="At least one query parameter (pid, sid, date, order, applytime, status, attendence) must be provided")
    appointments = get_appointment(db=db, pid=pid, sid=sid, date=date, order=order, applytime=applytime, status=status, attendence=attendence)
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found")
    return {"appointment": appointments}