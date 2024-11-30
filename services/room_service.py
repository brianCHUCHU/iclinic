from sqlalchemy.orm import Session
from models.room import Room
from schemas.room import RoomCreate, RoomUpdate
from fastapi import HTTPException
from passlib.context import CryptContext

def create_room(db: Session, room_data: RoomCreate):
    existing_room = db.query(Room).filter_by(rid=room_data.rid, cid=room_data.cid).first()
    if existing_room:
        return None

    new_room = Room(
        rid=room_data.rid,
        cid=room_data.cid,
        rname=room_data.rname,
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

def update_room_name(db: Session, cid: str, rid: str, new_name: str):
    try:
        room = db.query(Room).filter_by(cid=cid, rid=rid).one()
        room.rname = new_name
        db.commit()
        db.refresh(room)
        return room
    except NoResultFound:
        return None