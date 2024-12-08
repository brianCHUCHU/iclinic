from sqlalchemy.orm import Session
from models import Appointment
from schemas.appointment import AppointmentCreate ,AppointmentUpdate
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm.exc import NoResultFound

def create_appointment(db: Session, appointment_data: AppointmentCreate):
    existing_appointment = db.query(Appointment).filter_by(
        pid=appointment_data.pid,
        sid=appointment_data.sid,
        date=appointment_data.date,
        order=appointment_data.order
    ).first()
    if existing_appointment:
        return HTTPException(status_code=400, detail="Appointment already exists")
    appointment_dict = appointment_data.model_dump()
    new_appointment = Appointment(**appointment_dict)

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return {"message": "Appointment created successfully","appointment":new_appointment}

def update_appointment(db: Session, pid: str, sid: str, date: str, order: int, new: AppointmentUpdate):
    appointment = db.query(Appointment).filter_by(
        pid=pid,
        sid=sid,
        date=date,
        order=order
    ).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment_data = new.model_dump()
    for key ,value in appointment_data.items():
        setattr(appointment ,key ,value)
    db.commit()
    db.refresh(appointment)
    return {"message": "Appointment name updated successfully", "appointment": appointment}

def get_appointment(
        db: Session, 
        pid: str, 
        sid: str, 
        date : str, 
        order : int, 
        applytime: str = None,
        status : str = None,
        attendance : str = None
    ):
    query = db.query(Appointment)
    if pid:
        query = query.filter(Appointment.pid == pid)
    if sid:
        query = query.filter(Appointment.sid == sid)
    if date:
        query = query.filter(Appointment.date == date)
    if order:
        query = query.filter(Appointment.order == order)
    if applytime:
        query = query.filter(Appointment.applytime == applytime)
    if status:
        query = query.filter(Appointment.status == status)    
    if attendance:
        query = query.filter(Appointment.attendance == attendance)
    appointments = query.all()
    if not appointments:
        raise HTTPException(status_code=404, detail="No Appointments found")
    return appointments