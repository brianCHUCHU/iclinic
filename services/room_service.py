from sqlalchemy.orm import Session
from models import Room, Roomschedule
from schemas.room import RoomCreate ,RoomUpdate
from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound

def create_room(db: Session, room_data: RoomCreate):
    existing_room = db.query(Room).filter_by(rid=room_data.rid, cid=room_data.cid).first()
    if existing_room:
        raise HTTPException(status_code=400, detail="Room already exists")
    room_dict = room_data.model_dump()
    new_room = Room(**room_dict)

    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return {"message": "Room created successfully","room":new_room}

def update_room_name(db: Session, rid: str, new_name: RoomUpdate):
    room = db.query(Room).filter_by(rid=rid).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if new_name.rname:
        room.rname = new_name.rname
    if new_name.available is not None:
        room.available = new_name.available
    db.commit()
    db.refresh(room)
    return {"message": "Room name updated successfully", "room": room}

def get_room(db: Session, rid: str = None, cid: str = None, rname: str = None):
    query = db.query(Room)
    if rid:
        query = query.filter(Room.rid == rid)
    if cid:
        query = query.filter(Room.cid == cid)
    if rname:
        query = query.filter(Room.rname == rname)
    rooms = query.all()
    if not rooms:
        raise HTTPException(status_code=404, detail="No rooms found")
    return rooms
