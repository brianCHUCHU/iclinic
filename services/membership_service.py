from sqlalchemy.orm import Session
from models import Membership
from schemas.patient import MembershipCreate, MembershipUpdate
from fastapi import HTTPException

# 創建會員
def create_membership(db: Session, membership_data: MembershipCreate):
    new_member = Membership(**membership_data.model_dump())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

# 查詢會員 (根據 pid 或帳號名稱)
def get_membership(db: Session, pid: str = None):
    if pid:
        return db.query(Membership).filter(Membership.pid == pid).first()
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
