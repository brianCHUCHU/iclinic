from sqlalchemy.orm import Session
from models.division import Division
from schemas.division import DivisionCreate

def create_division(db: Session, division_data: DivisionCreate):
    db_division = Division(divid=division_data.divid, divname=division_data.divname)
    db.add(db_division)
    db.commit()
    db.refresh(db_division)
    return db_division

def update_division(db: Session, divid: str, division_update: DivisionCreate):
    db_division = db.query(Division).filter(Division.divid == divid).first()
    if db_division:
        db_division.divname = division_update.divname
        db.commit()
        db.refresh(db_division)
        return db_division
    return None


def delete_division(db: Session, divid: str):
    db_division = db.query(Division).filter(Division.divid == divid).first()
    if db_division:
        db.delete(db_division)
        db.commit()
        return db_division
    return None

def get_division_by_id(db: Session, divid: str):
    return db.query(Division).filter(Division.divid == divid).first()

def get_division_by_name(db: Session, divname: str):
    return db.query(Division).filter(Division.divname == divname).first()
