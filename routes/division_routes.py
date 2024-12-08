from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.division_service import create_division, update_division, delete_division, get_division
from utils.db import get_db
from schemas.division import DivisionCreate

division_router = APIRouter()

@division_router.post("/divisions", status_code=201)
def create_division_endpoint(division: DivisionCreate, db: Session = Depends(get_db)):
    
    result = create_division(db=db, division_data=division)
    return result  # Returns the result from the service layer, which includes division id


# get division by id
@division_router.get("/divisions")
def get_division_endpoint(db: Session = Depends(get_db), divid: str = None, divname: str = None):
    if divid:
        division = get_division(db=db, divid=divid)
    elif divname:
        division = get_division(db=db, divname=divname)
    else:
        raise HTTPException(status_code=400, detail="Invalid query parameters")
    if not division:
        raise HTTPException(status_code=404, detail="Division not found")
    return division