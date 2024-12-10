from sqlalchemy.orm import Session
from models import Membership, Patient
from schemas.patient import MembershipCreate, MembershipUpdate
from fastapi import HTTPException

# 創建會員
def create_membership(db: Session, membership_data: MembershipCreate):
    new_patient = Patient(
        pid=membership_data.pid,
        pname=membership_data.pname,
        birthdate=membership_data.birthdate,
        status=membership_data.status,
        gender=membership_data.gender)
    
    # add only pid, acct, email to membership
    new_member = Membership(
        pid=membership_data.pid,
        acct_pw=membership_data.acct_pw,
        email=membership_data.email)
    
    try:
        db.add(new_patient)
        db.add(new_member)
        db.commit()
        db.refresh(new_member)
        db.refresh(new_patient)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return new_member

# 查詢會員 (根據 pid 或帳號名稱)
<<<<<<< HEAD
def get_membership(db: Session, pid: str = None, acct_name: str = None):
    if pid:
        return db.query(Membership).filter(Membership.pid == pid).first()
    if acct_name:
        return db.query(Membership).filter(Membership.acct_name == acct_name).first()
=======
def get_membership(db: Session, pid: str = None):
    if pid:
        return db.query(Membership).filter(Membership.pid == pid).first()
>>>>>>> afdfb08053d764e00433128a353975515f103e97
    return None

# 更新會員資料
def update_membership(db: Session, membership_update: MembershipUpdate):
    member = get_membership(db, pid=membership_update.pid)
    if not member:
        raise HTTPException(status_code=404, detail="Membership not found")
    for key, value in membership_update.dict(exclude_unset=True).items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member

# 刪除會員
def delete_membership(db: Session, pid: str):
    member = get_membership(db, pid=pid)
    if not member:
        raise HTTPException(status_code=404, detail="Membership not found")
    db.delete(member)
    db.commit()
    return member
