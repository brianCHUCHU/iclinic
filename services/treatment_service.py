from sqlalchemy.orm import Session
from ..models.treatment import Treatment
from ..schemas.treatment import TreatmentCreate ,TreatmentUpdate

def create_treatment(db: Session, treatment_data: TreatmentCreate):
    existing_treatment = db.query(Treatment).filter_by(sid=treatment_data.sid).first()
    if existing_treatment:
        return None

    new_treatment = Treatment(
        tid = treatment_data.tid,
        docid=treatment_data.docid,
        divid=treatment_data.divid,
        cid=treatment_data.cid,
        tname=treatment_data.tname,
    )
    db.add(new_treatment)
    db.commit()
    db.refresh(new_treatment)
    return new_treatment

def update_treatment_name(db: Session, tid: str, new_name: TreatmentUpdate):
    treatment = db.query(Treatment).filter_by(tid=tid).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    if new_name.tname:
        treatment.tname = new_name.tname
    if new_name.available:
        treatment.available = new_name.available
    db.commit()
    db.refresh(treatment)
    return {"message": "Treatment name updated successfully", "treatment": treatment}

def get_treatment(
        db: Session, 
        tid: str = None, 
        docid: str = None, 
        divid : str = None , 
        cid : str = None , 
        tname: str = None
    ):
    query = db.query(Treatment)
    if tid:
        query = query.filter(Treatment.tid == tid)
    if docid:
        query = query.filter(Treatment.docid == docid)
    if divid:
        query = query.filter(Treatment.divid == divid)
    if cid:
        query = query.filter(Treatment.cid == cid)
    if tname:
        query = query.filter(Treatment.tname == tname)
    treatments = query.all()
    if not treatments:
        raise HTTPException(status_code=404, detail="No treatments found")
    return treatments