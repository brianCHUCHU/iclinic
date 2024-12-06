from pydantic import BaseModel, EmailStr
from typing import Optional

class MembershipBase(BaseModel):
    pid: str  # Patient ID
    acctname: str
    email: EmailStr

class MembershipCreate(MembershipBase):
    acctpw: str  # Plain text password, will be hashed before storage

class MembershipUpdate(MembershipBase):
    acctname: Optional[str]
    email: Optional[EmailStr]
    acctpw: Optional[str]  # Allows partial updates, e.g., just updating the password

class Membership(MembershipBase):
    acctpw: str  # Member Account Password

    class Config:
        orm_mode = True

