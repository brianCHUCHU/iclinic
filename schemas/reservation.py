from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class ReservationBase(BaseModel):
    pid : str
    sid : str
    date : str
    applytime : str
    tid : str
    status : str
    attendence : bool

class ReservationCreate(ReservationBase):
    status : str = "P"
    attendence : bool = True

class ReservationUpdate(ReservationBase):
    pid : str
    sid : str 
    date : str
    applytime : str
    tid : str = None
    status : str = None
    attendence : bool = None