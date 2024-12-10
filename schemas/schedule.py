from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class ScheduleBase(BaseModel):
    divid : str
    perid : str
    docid : str
    available : bool

class ScheduleCreate(ScheduleBase):
    available : bool = True

class ScheduleUpdate(BaseModel):
    divid : str
    perid : str
    docid : str