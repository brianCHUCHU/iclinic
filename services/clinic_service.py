from sqlalchemy.orm import Session
from models import Clinic
from schemas.clinic import ClinicCreate, ClinicUpdate
from fastapi import HTTPException

def create_clinic(db: Session, clinic_data: ClinicCreate):
    existing_clinic = db.query(Clinic).filter_by(cid=clinic_data.cid).first()
    if existing_clinic:
        raise HTTPException(status_code=400, detail="Clinic already exists")
    
    # 創建新的診所物件，並將來自 schema 的資料傳入
    clinic_dict = clinic_data.model_dump()
    new_clinic = Clinic(**clinic_dict)  # Now pass the updated dictionary

    # 添加到資料庫並提交
    db.add(new_clinic)
    db.commit()
    db.refresh(new_clinic)
    
    # 返回新的診所資料或消息
    return {"message": "Clinic created successfully", "clinic": new_clinic.cid}


# 查詢診所 (單一)
def get_clinic_by_id(db: Session, cid: str):
    return db.query(Clinic).filter(Clinic.cid == cid).first()

# 更新診所資料
def update_clinic(db: Session, cid: str, clinic_update: ClinicUpdate):
    clinic = get_clinic_by_id(db, cid)
    if not clinic:
        return None
    for key, value in clinic_update.model_dump(exclude_unset=True).items():
        setattr(clinic, key, value)
    db.commit()
    db.refresh(clinic)
    return clinic

# 刪除診所
def delete_clinic(db: Session, cid: str):
    clinic = get_clinic_by_id(db, cid)
    if not clinic:
        return None
    db.delete(clinic)
    db.commit()
    return clinic

def get_clinic_by_acct_name(db: Session, acct_name: str):
    return db.query(Clinic).filter(Clinic.acct_name == acct_name).first()

# 查詢所有診所 (支援條件篩選)
def get_all_clinics(db: Session, city: str = None, district: str = None):
    query = db.query(Clinic)
    if city:
        query = query.filter(Clinic.city == city)
    if district:
        query = query.filter(Clinic.district == district)
    return query.all()
