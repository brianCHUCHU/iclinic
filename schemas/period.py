from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class PeriodBase(BaseModel):
    perid : str
    cid : str
    weekday : str
    starttime : str
    endtime: str
    available : bool

class PeriodCreate(PeriodBase):
    available : bool = True

class PeriodUpdate(PeriodBase):
    perid : str
    cid : str = None
    weekday : str = None
    starttime : str = None
    endtime : str = None
    available : bool = None