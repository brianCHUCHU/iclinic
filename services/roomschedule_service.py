from sqlalchemy.orm import Session
from models import Roomschedule, Room, Schedule
from schemas.roomschedule import RoomScheduleCreate, RoomScheduleUpdate
from fastapi import HTTPException


def create_room_schedule(db: Session, room_schedule_data: RoomScheduleCreate):
    existing_room_schedule = db.query(Roomschedule).filter_by(rid=room_schedule_data.rid, cid=room_schedule_data.cid, sid=room_schedule_data.sid).first()
    if existing_room_schedule:
        raise HTTPException(status_code=400, detail="Room schedule already exists")
    if not db.query(Room).filter_by(rid=room_schedule_data.rid, cid = room_schedule_data.cid).first():
        raise HTTPException(status_code=404, detail="Room not found")

    room_schedule_dict = room_schedule_data.model_dump()
    new_room_schedule = Roomschedule(**room_schedule_dict)

    db.add(new_room_schedule)
    db.commit()
    db.refresh(new_room_schedule)
    return {"message": "Room schedule created successfully", "room_schedule": new_room_schedule}

def enable_room_schedule(db: Session, room_schedule_data: RoomScheduleUpdate):
    room_schedule = db.query(Roomschedule).filter_by(rid=room_schedule_data.rid, cid=room_schedule_data.cid, sid=room_schedule_data.sid).first()
    if not room_schedule:
        raise HTTPException(status_code=404, detail="Room schedule not found")
    room_schedule.available = True
    db.commit()
    db.refresh(room_schedule)
    return {"message": "Room schedule enabled successfully", "room_schedule": room_schedule}

def disable_room_schedule(db: Session, room_schedule_data: RoomScheduleUpdate):
    room_schedule = db.query(Roomschedule).filter_by(rid=room_schedule_data.rid, cid=room_schedule_data.cid, sid=room_schedule_data.sid).first()
    if not room_schedule:
        raise HTTPException(status_code=404, detail="Room schedule not found")
    room_schedule.available = False
    db.commit()
    db.refresh(room_schedule)
    return {"message": "Room schedule disabled successfully", "room_schedule": room_schedule}

def delete_room_schedule(db: Session, room_schedule_data: RoomScheduleUpdate):
    room_schedule = db.query(Roomschedule).filter_by(rid=room_schedule_data.rid, cid=room_schedule_data.cid, sid=room_schedule_data.sid).first()
    if not room_schedule:
        raise HTTPException(status_code=404, detail="Room schedule not found")
    db.delete(room_schedule)
    db.commit()
    return {"message": "Room schedule deleted successfully"}