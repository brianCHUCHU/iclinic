from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.treatment import Treatment
from services.treatment_service import create_treatment ,update_treatment ,get_treatment
from utils.db import get_db
from schemas.treatment import TreatmentCreate ,TreatmentUpdate

treatment_router = APIRouter()

@treatment_router.post("/treatment", status_code=201)
def create_treatment_endpoint(treatment: TreatmentCreate ,db: Session = Depends(get_db)):
    result = create_treatment(db= db ,treatment_data= treatment)
    return result

@treatment_router.put("/treatment", status_code=200)
def update_treatment_endpoint(treatment: TreatmentUpdate, db: Session = Depends(get_db)):
    result = update_treatment(db=db, tid=treatment.tid, new=treatment)
    return result

@treatment_router.get("/treatment")
def get_treatment_endpoint(
    db: Session = Depends(get_db),
    tid: str = None, 
    docid: str = None, 
    divid : str = None , 
    cid : str = None , 
    tname: str = None
):
    if not any([tid, docid, divid, cid, tname]):
        raise HTTPException(status_code=400, detail="At least one query parameter (tid, docid, divid, cid, tname) must be provided")
    treatments = get_treatment(db=db, tid=tid, docid=docid, divid=divid, cid=cid, tname= tname)
    if not treatments:
        raise HTTPException(status_code=404, detail="No treatments found")
    return {"treatment": treatments}