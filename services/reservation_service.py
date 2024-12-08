from sqlalchemy.orm import Session
from models import Reservation
from schemas.reservation import ReservationCreate ,ReservationUpdate
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm.exc import NoResultFound

def create_reservation(db: Session, reservation_data: ReservationCreate):
    existing_reservation = db.query(Reservation).filter_by(
        pid=reservation_data.pid,
        sid=reservation_data.sid,
        date=reservation_data.date,
        applytime=reservation_data.applytime
    ).first()
    if existing_reservation:
        return HTTPException(status_code=400, detail="Reservation already exists")
    reservation_dict = reservation_data.model_dump()
    new_reservation = Reservation(**reservation_dict)

    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return {"message": "Reservation created successfully","reservation":new_reservation}

def update_reservation(db: Session, pid: str, sid: str, date: str, applytime: int, new: ReservationUpdate):
    reservation = db.query(Reservation).filter_by(
        pid=pid,
        sid=sid,
        date=date,
        applytime=applytime
    ).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    reservation_data = new.model_dump()
    for key ,value in reservation_data.items():
        if value is not None:
            setattr(reservation ,key ,value)
    db.commit()
    db.refresh(reservation)
    return {"message": "Reservation name updated successfully", "reservation": reservation}

def get_reservation(
        db: Session, 
        pid: str, 
        sid: str, 
        date : str, 
        applytime : str, 
        tid: str = None,
        status : str = None,
        attendance : str = None
    ):
    query = db.query(Reservation)
    if pid:
        query = query.filter(Reservation.pid == pid)
    if sid:
        query = query.filter(Reservation.sid == sid)
    if date:
        query = query.filter(Reservation.date == date)
    if applytime:
        query = query.filter(Reservation.applytime == applytime)
    if tid:
        query = query.filter(Reservation.tid == tid)
    if status:
        query = query.filter(Reservation.status == status)    
    if attendance:
        query = query.filter(Reservation.attendance == attendance)
    reservations = query.all()
    if not reservations:
        raise HTTPException(status_code=404, detail="No Reservations found")
    return reservations