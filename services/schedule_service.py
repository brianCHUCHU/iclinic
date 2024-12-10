from sqlalchemy.orm import Session
from models import Schedule
from schemas.schedule import ScheduleCreate ,ScheduleUpdate
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm.exc import NoResultFound

def random_schedule_id(db: Session):
    import random
    import string
    # start with C and followed by 9 random numbers (digits only)
    sid = "S" + ''.join(random.choices(string.digits, k=9))
    while db.query(Schedule).filter(Schedule.sid == sid).first():
        sid = "S" + ''.join(random.choices(string.digits, k=9))
    return sid

def create_schedule(db: Session, schedule_data: ScheduleCreate):
    sid = random_schedule_id(db)
    schedule_dict = schedule_data.model_dump()
    new_schedule = Schedule(**schedule_dict)
    new_schedule.sid = sid

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return {"message": "Schedule created successfully","Schedule":new_schedule}

def enable_schedule(db: Session, data: ScheduleUpdate):
    schedule = db.query(Schedule).filter_by(docid=data.docid, divid=data.divid, perid=data.perid).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    schedule.available = True
    db.commit()
    db.refresh(schedule)
    return {"message": "Schedule enabled successfully", "schedule": schedule}

def disable_schedule(db: Session, data: ScheduleUpdate):
    schedule = db.query(Schedule).filter_by(docid=data.docid, divid=data.divid, perid=data.perid).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    schedule.available = False
    db.commit()
    db.refresh(schedule)
    return {"message": "Schedule disabled successfully", "schedule": schedule}

def get_schedule(
        db: Session, 
        sid: str = None, 
        divid: str = None, 
        perid : str = None , 
        docid : str = None , 
        available: bool = None
    ):
    query = db.query(Schedule)
    if sid:
        query = query.filter(Schedule.sid == sid)
    if divid:
        query = query.filter(Schedule.divid == divid)
    if perid:
        query = query.filter(Schedule.perid == perid)
    if docid:
        query = query.filter(Schedule.docid == docid)
    if available:
        query = query.filter(Schedule.available == available)
    schedules = query.all()
    if not schedules:
        raise HTTPException(status_code=404, detail="No schedules found")
    return schedules



