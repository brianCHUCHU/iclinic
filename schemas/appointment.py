from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class AppointmentBase(BaseModel):
    pid : str
    sid : str
    date : str
    order : int
    applytime : str
    status : str
    attendance : bool

class AppointmentCreate(AppointmentBase):
    status : str = "P"
    attendance : bool = False

class AppointmentUpdate(AppointmentBase):
    pid : str
    sid : str 
    date : str
    order : int
    applytime : str = None
    status : str = None
    attendance : bool = None