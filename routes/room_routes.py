from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.room import Room
from services.room_service import create_room ,update_room_name
from utils.db import get_db
from schemas.room import RoomCreate ,RoomUpdate

room_router = APIRouter()

@room_router.post("/room", status_code=201)
def create_room_endpoint(room: RoomCreate, db: Session = Depends(get_db)):
    result = create_room(db=db, room_data=room)
    return result

@room_router.put("/room", status_code=200)
def update_room_name_endpoint(room: RoomUpdate, db: Session = Depends(get_db)):
    room_to_update = db.query(Room).filter(room.rid == room.rid).first()
    
    if not room_to_update:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room_to_update.rname = room.rname
    db.commit()
    db.refresh(room_to_update)

    return {"message": "Room name updated successfully", "room": room_to_update}
