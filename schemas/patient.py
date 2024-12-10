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
<<<<<<< HEAD
    status: str = 'M'
=======
>>>>>>> afdfb08053d764e00433128a353975515f103e97
    acct_pw: str
    email: str

class MembershipUpdate(BaseModel):
    pid: str
    acct_pw: Optional[str]
    email: Optional[str]

class MembershipAuth(BaseModel):
    pid: str
    acct_pw: str