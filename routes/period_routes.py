from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Period
from services.period_service import create_period ,update_period ,get_period
from utils.db import get_db
from schemas.period import PeriodCreate ,PeriodUpdate

period_router = APIRouter()

@period_router.post("/period", status_code=201)
def create_period_endpoint(period: PeriodCreate ,db: Session = Depends(get_db)):
    result = create_period(db= db ,period_data= period)
    return result

@period_router.put("/period", status_code=200)
def update_period_endpoint(period: PeriodUpdate, db: Session = Depends(get_db)):
    result = update_period(db=db, perid=period.perid, new=period)
    return result

@period_router.get("/period")
def get_period_endpoint(
    db: Session = Depends(get_db),
    perid: str = None, 
    cid: str = None, 
    weekday : str = None , 
    starttime : str = None , 
    endtime: str = None,
    available : str = None
):
    if not any([perid, cid, weekday, starttime, endtime ,available]):
        raise HTTPException(status_code=400, detail="At least one query parameter (perid, cid, weekday, starttime, endtime ,available) must be provided")
    periods = get_period(db=db, perid=perid, cid=cid, weekday=weekday, starttime=starttime, endtime=endtime ,available=available)
    if not periods:
        raise HTTPException(status_code=404, detail="No periods found")
    return {"period": periods}