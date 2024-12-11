from sqlalchemy.orm import Session
from models import Period
from schemas.period import PeriodCreate ,PeriodUpdate
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm.exc import NoResultFound

def create_period(db: Session, period_data: PeriodCreate):
    import random
    import string

    # Generate a unique random room ID
    def generate_random_room_id():
        rid = "P" + ''.join(random.choices(string.digits, k=9))
        while db.query(Period).filter(Period.perid == rid).first():
            rid = "P" + ''.join(random.choices(string.digits, k=9))
        return rid
    period_dict = period_data.model_dump()
    new_period = Period(**period_dict)
    new_period.perid = generate_random_room_id()
    db.add(new_period)
    db.commit()
    db.refresh(new_period)
    return {"message": "Period created successfully","period":new_period}

# def update_period(db: Session, perid: str, new: PeriodUpdate):
#     period = db.query(Period).filter_by(perid=perid).first()
#     if not period:
#         raise HTTPException(status_code=404, detail="Period not found")
#     if new.weekday:
#         period.weekday = new.weekday
#     if new.starttime:
#         period.starttime = new.starttime
#     if new.endtime:
#         period.endtime = new.endtime
#     if new.available is not None:
#         period.available = new.available
#     db.commit()
#     db.refresh(period)
#     return {"message": "Period name updated successfully", "period": period}

def update_period(db: Session, perid: str, new: PeriodUpdate):
    period = db.query(Period).filter_by(perid=perid).first()
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    period_data = new.model_dump()
    for key ,value in period_data.items():
        setattr(period ,key ,value)
    db.commit()
    db.refresh(period)
    return {"message": "Period name updated successfully", "period": period}

def get_period(
        db: Session, 
        perid: str = None, 
        cid: str = None, 
        weekday : str = None , 
        starttime : str = None , 
        endtime: str = None,
        available : str = None
    ):
    query = db.query(Period)
    if perid:
        query = query.filter(Period.perid == perid)
    if cid:
        query = query.filter(Period.cid == cid)
    if weekday:
        query = query.filter(Period.weekday == weekday)
    if starttime:
        query = query.filter(Period.starttime == starttime)
    if endtime:
        query = query.filter(Period.endtime == endtime)
    if available:
        query = query.filter(Period.available == available)
    periods = query.all()
    if not periods:
        raise HTTPException(status_code=404, detail="No Periods found")
    return periods
