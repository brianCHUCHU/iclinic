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

class MembershipCreate(BaseModel):
    pid: str
    acctpw: str
    email: str

class MembershipUpdate(BaseModel):
    pid: str
    acctpw: Optional[str]
    email: Optional[str]

class MembershipAuth(BaseModel):
    pid: str
    acctpw: str