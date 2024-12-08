from sqlalchemy.orm import Session
from models import Clinic
from schemas.clinic import ClinicCreate, ClinicUpdate
from fastapi import HTTPException
from passlib.context import CryptContext

# 密碼加密工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_clinic(db: Session, clinic_data: ClinicCreate):
    existing_clinic = db.query(Clinic).filter_by(cid=clinic_data.cid).first()
    if existing_clinic:
        raise HTTPException(status_code=400, detail="Clinic already exists")

    # 密碼加密
    hashed_password = pwd_context.hash(clinic_data.acct_pw)
    
    # 創建新的診所物件，並將來自 schema 的資料傳入
    clinic_dict = clinic_data.model_dump()
    clinic_dict['acct_pw'] = hashed_password  # Modify the password here
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

# 登入功能 (驗證帳密)
def authenticate_clinic(db: Session, acct_name: str, password: str):
    clinic = db.query(Clinic).filter(Clinic.acct_name == acct_name).first()
    if not clinic or not pwd_context.verify(password, clinic.acct_pw):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return clinic

# 更新診所資料
def update_clinic(db: Session, cid: str, clinic_update: ClinicUpdate):
    clinic = get_clinic_by_id(db, cid)
    if not clinic:
        return None
    for key, value in clinic_update.model_dump(exclude_unset=True).items():
        if key == "acct_pw":
            value = pwd_context.hash(value)  # 更新密碼需重新加密
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

# 查詢所有診所 (支援條件篩選)
def get_all_clinics(db: Session, city: str = None, district: str = None):
    query = db.query(Clinic)
    if city:
        query = query.filter(Clinic.city == city)
    if district:
        query = query.filter(Clinic.district == district)
    return query.all()
