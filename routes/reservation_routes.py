from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.reservation import Reservation
from services.reservation_service import create_reservation ,update_reservation ,get_reservation
from utils.db import get_db
from schemas.reservation import ReservationCreate ,ReservationUpdate

reservation_router = APIRouter()

@reservation_router.post("/reservation", status_code=201)
def create_reservation_endpoint(reservation: ReservationCreate ,db: Session = Depends(get_db)):
    result = create_reservation(db= db ,reservation_data= reservation)
    return result

@reservation_router.put("/reservation", status_code=200)
def update_reservation_endpoint(reservation: ReservationUpdate, db: Session = Depends(get_db)):
    result = update_reservation(db=db, pid=reservation.pid, new=reservation)
    return result

@reservation_router.get("/reservation")
def get_reservation_endpoint(
    db: Session = Depends(get_db),
    pid: str = None, 
    sid: str = None, 
    date : str = None , 
    applytime : str = None , 
    tid: str = None,
    status : str = None,
    attendence : str = None
):
    if not any([pid, sid, date, applytime, tid ,status, attendence]):
        raise HTTPException(status_code=400, detail="At least one query parameter (pid, sid, date, applytime, tid, status, attendence) must be provided")
    reservations = get_reservation(db=db, pid=pid, sid=sid, date=date, applytime=applytime, tid=tid, status=status, attendence=attendence)
    if not reservations:
        raise HTTPException(status_code=404, detail="No reservations found")
    return {"reservation": reservations}