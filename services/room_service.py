from sqlalchemy.orm import Session
from models.room import Room
from schemas.room import RoomCreate ,RoomUpdate
from fastapi import HTTPException
from passlib.context import CryptContext

def create_room(db: Session, room_data: RoomCreate):
    existing_room = db.query(Room).filter_by(rid=room_data.rid, cid=room_data.cid).first()
    if existing_room:
        raise HTTPException(status_code=400, detail="Room already exists")

    new_room = Room(
        rid=room_data.rid,
        cid=room_data.cid,
        rname=room_data.rname,
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return {"message": "Room created successfully","room":new_room}

def update_room_name(db: Session, rid: str, new_name: RoomUpdate):
    room = db.query(Room).filter_by(rid=rid).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room.rname = new_name.rname
    db.commit()
    db.refresh(room)
    return {"message": "Room name updated successfully", "room": room}
