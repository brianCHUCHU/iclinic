from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Schedule
from services.schedule_service import create_schedule ,enable_schedule ,get_schedule, disable_schedule
from utils.db import get_db
from schemas.schedule import ScheduleCreate ,ScheduleUpdate

schedule_router = APIRouter()

# @schedule_router.post("/schedule", status_code=201)
# def create_schedule_endpoint(schedule: ScheduleCreate ,db: Session = Depends(get_db)):
#     result = create_schedule(db= db ,schedule_data= schedule)
#     return result

# @schedule_router.put("/schedule", status_code=200)
# def update_schedule_endpoint(schedule: ScheduleUpdate, db: Session = Depends(get_db)):
#     result = update_schedule(db=db, sid=schedule.sid, new=schedule)
#     return result

# @schedule_router.get("/schedule")
# def get_schedule_endpoint(
#     db: Session = Depends(get_db),
#     sid: str = None, 
#     divid: str = None, 
#     perid : str = None , 
#     docid : str = None , 
#     available: bool = None
# ):
#     if not any([sid, divid, perid, docid, available]):
#         raise HTTPException(status_code=400, detail="At least one query parameter (sid, divid, perid, docid, available) must be provided")
#     schedules = get_schedule(db=db, sid=sid, divid=divid, perid=perid, docid=docid, available= available)
#     if not schedules:
#         raise HTTPException(status_code=404, detail="No schedules found")
#     return {"schedule": schedules}