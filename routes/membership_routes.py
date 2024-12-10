from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from services.membership_service import create_membership, update_membership, delete_membership, get_membership
from utils.db import get_db
from schemas.patient import MembershipCreate, MembershipUpdate, MembershipAuth
import utils.security as sec

membership_router = APIRouter()

@membership_router.post("/memberships", status_code=201)
def create_membership_endpoint(membership: MembershipCreate, db: Session = Depends(get_db)):
    # hash the password
    try:
        membership.acct_pw = sec.hash_password(membership.acct_pw)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    result = create_membership(db=db, membership_data=membership)
    return {"message": "Membership created successfully", "membership": result.pid}

# update membership
@membership_router.put("/memberships/{pid}")
def update_membership_endpoint(pid: str, membership: MembershipUpdate, db: Session = Depends(get_db)):
    if membership.acct_pw:
        membership.acct_pw = sec.hash_password(membership.acct_pw)
    result = update_membership(db=db, membership_update=membership)
    if not result:
        raise HTTPException(status_code=404, detail="Membership not found")

    return {"message": "Membership updated successfully", "membership": result.pid}

# delete membership
@membership_router.delete("/memberships/{pid}")
def delete_membership_endpoint(pid: str, db: Session = Depends(get_db)):
    result = delete_membership(db=db, pid=pid)
    if not result:
        raise HTTPException(status_code=404, detail="Membership not found")

    return {"message": "Membership deleted successfully", "membership": result.pid}

# get membership by id
@membership_router.get("/memberships/{pid}")
def get_membership_endpoint(pid: str, db: Session = Depends(get_db)):
    result = get_membership(db=db, pid=pid)
    if not result:
        raise HTTPException(status_code=404, detail="Membership not found")

    return result

@membership_router.post("/memberships/authenticate")
def authenticate_membership_endpoint(auth: MembershipAuth, request: Request, db: Session = Depends(get_db)):
    # 查找用户
    result = get_membership(db=db, pid=auth.pid)
    if not result:
        raise HTTPException(status_code=404, detail="Membership not found")
    if not sec.verify_password(auth.acct_pw, result.acct_pw):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 将用户信息存入会话
    session = request.session
    session['user_id'] = result.pid
    session['welcome_state'] = True
    session['record_state'] = False  # 初始化状态
    session['schedule_state'] = False  # 初始化状态
    session['pending_state'] = False
    
    return {"message": "Authentication successful", "membership": result.pid}