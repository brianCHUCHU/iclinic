from sqlalchemy.orm import Session
from ..models import Period
from ..schemas import PeriodCreate

def create_period(db: Session, period_data: PeriodCreate):
    existing_period = db.query(Period).filter_by(perid=period_data.perid).first()
    if existing_period:
        return None

    new_period = Period(
        perid=period_data.perid,
        cid=period_data.cid,
        weekday=period_data.weekday,
        starttime=period_data.starttime,
        endtime=period_data.endtime,
        available=period_data.available,
    )
    db.add(new_period)
    db.commit()
    db.refresh(new_period)
    return new_period

def update_period_availability(db: Session, perid: str, availability: bool):
    period = db.query(Period).filter_by(perid=perid).first()
    if not period:
        return None

    period.available = availability
    db.commit()
    db.refresh(period)
    return period

