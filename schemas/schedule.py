from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class ScheduleBase(BaseModel):
    sid : str
    divid : str
    perid : str
    docid : str
    available : bool

class ScheduleCreate(ScheduleBase):
    available : bool = True

class ScheduleUpdate(ScheduleBase):
    sid : str
    divid : str = None
    perid : str = None
    docid : str = None
    available : bool