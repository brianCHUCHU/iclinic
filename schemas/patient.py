from pydantic import BaseModel
from datetime import date
from typing import Optional

class PatientBase(BaseModel):
    pname: str
    birthdate: date
    gender: str
    status: str

class PatientCreate(PatientBase):
    pid: str  # 需要額外的欄位

class PatientUpdate(BaseModel):
    pname: str = None
    birthdate: date = None
    gender: str = None
    status: str = None

class MembershipCreate(PatientBase):
    pid: str
    status: str = 'M'
    acct_pw: str
    email: str

class MembershipUpdate(BaseModel):
    pid: str
    acct_pw: Optional[str]
    email: Optional[str]

class MembershipAuth(BaseModel):
    pid: str
    acct_pw: str