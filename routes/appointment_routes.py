from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Appointment
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
    result = update_appointment(
        db=db,
        pid=appointment.pid,
        sid=appointment.sid,
        date=appointment.date,
        order=appointment.order,
        new=appointment)
    return result

@appointment_router.get("/appointment")
def get_appointment_endpoint(
    db: Session = Depends(get_db),
    pid: str = None, 
    sid: str = None, 
    date : str = None , 
    order : int = None , 
    applytime: str = None,
    status : str = None,
    attendance : str = None
):
    if not any([pid, sid, date, order, applytime ,status, attendance]):
        raise HTTPException(status_code=400, detail="At least one query parameter (pid, sid, date, order, applytime, status, attendance) must be provided")
    appointments = get_appointment(db=db, pid=pid, sid=sid, date=date, order=order, applytime=applytime, status=status, attendance=attendance)
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found")
    return {"appointment": appointments}