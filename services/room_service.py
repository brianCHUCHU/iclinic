from sqlalchemy.orm import Session
from models import Room, Roomschedule
from schemas.room import RoomCreate ,RoomUpdate, RoomUpdateQueue
from fastapi import HTTPException, Depends
from sqlalchemy.orm.exc import NoResultFound
from utils.db import get_db

def create_room(db: Session, room_data: RoomCreate):
    import random
    import string

    # Generate a unique random room ID
    def generate_random_room_id():
        rid = "R" + ''.join(random.choices(string.digits, k=9))
        while db.query(Room).filter(Room.rid == rid).first():
            rid = "R" + ''.join(random.choices(string.digits, k=9))
        return rid

    # Convert RoomCreate to dictionary and create a new Room entry
    room_dict = room_data.model_dump()
    new_room = Room(**room_dict)
    new_room.rid = generate_random_room_id()

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return {"message": "Room created successfully", "room": new_room}

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

def update_room_queuenumber(db: Session, queue_data: RoomUpdateQueue):
    room = db.query(Room).filter_by(rid=queue_data.rid).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room.queuenumber = queue_data.queuenumber
    room.lastupdate = queue_data.lastupdate
    db.commit()
    db.refresh(room)
    return {"message": "Room queue number updated successfully", "room": room}

def get_room_queuenumber(db: Session, rid: str = None):
    # get db via session
    db = next(get_db())
    query = db.query(Room)
    if rid:
        query = query.filter(Room.rid == rid)
    rooms = query.first()
    if not rooms:
        raise HTTPException(status_code=404, detail="No rooms found")

    # leave only rid, currentorder, lastupdate
    rooms = {key: value for key, value in rooms.__dict__.items() if key in ["rid", "queuenumber", "lastupdate"]}
    return rooms