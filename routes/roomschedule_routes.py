from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.roomschedule_service import create_room_schedule ,enable_room_schedule ,disable_room_schedule ,delete_room_schedule
from utils.db import get_db
from schemas.roomschedule import RoomScheduleCreate ,RoomScheduleUpdate

roomschedule_router = APIRouter()

@roomschedule_router.post("/roomschedule/create", status_code=201)
def create_room_schedule_endpoint(room_schedule: RoomScheduleCreate, db: Session = Depends(get_db)):
    result = create_room_schedule(db=db, room_schedule_data=room_schedule)
    return result

@roomschedule_router.put("/roomschedule/enable", status_code=200)
def enable_room_schedule_endpoint(room_schedule: RoomScheduleUpdate, db: Session = Depends(get_db)):
    result = enable_room_schedule(db=db, room_schedule_data=room_schedule)
    return result

@roomschedule_router.put("/roomschedule/disable", status_code=200)
def disable_room_schedule_endpoint(room_schedule: RoomScheduleUpdate, db: Session = Depends(get_db)):
    result = disable_room_schedule(db=db, room_schedule_data=room_schedule)
    return result

@roomschedule_router.delete("/roomschedule/delete", status_code=200)
def delete_room_schedule_endpoint(room_schedule: RoomScheduleUpdate, db: Session = Depends(get_db)):
    result = delete_room_schedule(db=db, room_schedule_data=room_schedule)
    return result