from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class AppointmentBase(BaseModel):
    pid : str
    sid : str
    date : str
    order : str
    applytime : str
    status : str
    attendence : bool

class AppointmentCreate(AppointmentBase):
    status : str = "P"
    attendence : bool = True

class AppointmentUpdate(AppointmentBase):
    pid : str
    sid : str 
    date : str
    order : str
    applytime : str = None
    status : str = None
    attendence : bool = None