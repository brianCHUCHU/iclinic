from sqlalchemy.orm import Session
from ..models.schedule import Schedule
from ..schemas import ScheduleCreate

def create_schedule(db: Session, schedule_data: ScheduleCreate):
    existing_schedule = db.query(Schedule).filter_by(sid=schedule_data.sid).first()
    if existing_schedule:
        return None

    new_schedule = Schedule(
        sid=schedule_data.sid,
        divid=schedule_data.divid,
        perid=schedule_data.perid,
        docid=schedule_data.docid,
        available=schedule_data.available,
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

def update_schedule_availability(db: Session, sid: str, availability: bool):
    schedule = db.query(Schedule).filter_by(sid=sid).first()
    if not schedule:
        return None

    schedule.available = availability
    db.commit()
    db.refresh(schedule)
    return schedule

