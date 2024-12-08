from sqlalchemy.orm import Session
from models.schedule import Schedule
from schemas.schedule import ScheduleCreate ,ScheduleUpdate
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm.exc import NoResultFound

def create_schedule(db: Session, schedule_data: ScheduleCreate):
    existing_schedule = db.query(Schedule).filter_by(sid=schedule_data.sid).first()
    if existing_schedule:
        return HTTPException(status_code=400, detail="Schedule already exists")
    schedule_dict = schedule_data.model_dump()
    new_schedule = Schedule(**schedule_dict)

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return {"message": "Schedule created successfully","Schedule":new_schedule}

def update_schedule(db: Session, sid: str, new: ScheduleUpdate):
    schedule = db.query(Schedule).filter_by(sid=sid).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    if new.available is not None:
        schedule.available = new.available
    db.commit()
    db.refresh(schedule)
    return {"message": "Schedule updated successfully", "schedule": schedule}

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



