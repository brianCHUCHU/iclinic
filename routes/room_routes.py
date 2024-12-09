from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.room_service import create_room ,update_room_name ,get_room, get_room_queuenumber, update_room_queuenumber
from utils.db import get_db
from schemas.room import RoomCreate ,RoomUpdate, RoomUpdateQueue

room_router = APIRouter()

@room_router.post("/room", status_code=201)
def create_room_endpoint(room: RoomCreate, db: Session = Depends(get_db)):
    result = create_room(db=db, room_data=room)
    return result

@room_router.put("/room", status_code=200)
def update_room_name_endpoint(room: RoomUpdate, db: Session = Depends(get_db)):
    result = update_room_name(db=db, rid=room.rid, new_name=room)
    return result

@room_router.get("/rooms")
def get_room_endpoint(
    db: Session = Depends(get_db),
    rid: str = None,
    cid: str = None,
    rname: str = None
):
    if not any([rid, cid, rname]):
        raise HTTPException(status_code=400, detail="At least one query parameter (rid, cid, or rname) must be provided")
    rooms = get_room(db=db, rid=rid, cid=cid, rname=rname)
    if not rooms:
        raise HTTPException(status_code=404, detail="No rooms found")
    return {"rooms": rooms}

@room_router.get("/room/queuenumber/{rid}")
def get_room_queue_number(rid: str, db: Session = Depends(get_db)):
    result = get_room_queuenumber(db=db, rid=rid)
    return result

@room_router.put("/room/queuenumber", status_code=200)
def update_room_queue_number(room: RoomUpdateQueue, db: Session = Depends(get_db)):
    result = update_room_queuenumber(db=db, queue_data=room)
    return result