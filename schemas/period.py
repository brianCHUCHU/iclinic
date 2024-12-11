from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class PeriodBase(BaseModel):
    perid : str
    cid : str
    weekday : int
    starttime : str
    endtime: str
    available : bool

class PeriodCreate(BaseModel):
    cid : str
    weekday : int
    starttime : str
    endtime: str
    available : bool = True

class PeriodUpdate(PeriodBase):
    perid : str
    cid : str = None
    weekday : int = None
    starttime : str = None
    endtime : str = None
    available : bool = None