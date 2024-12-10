from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel

class ClinicBase(BaseModel):
    fee: int
    queue_type: str
    acct_name: str
    cname: str
    city: str
    district: str
    address: str
    available : bool

class ClinicCreate(ClinicBase):
    cid: str
    acct_pw: str
    available : bool = True

class ClinicUpdate(BaseModel):
    fee: int = None
    queue_type: str = None
    acct_name: str = None
    acct_pw: str = None
    cname: str = None
    city: str = None
    district: str = None
    address: str = None
    available : bool = None

class ClinicAuth(BaseModel):
    acct_name: str
    password: str

