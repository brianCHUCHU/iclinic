from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel

class RoomScheduleBase(BaseModel):
    rid : str
    cid : str
    sid : str

class RoomScheduleCreate(RoomScheduleBase):
    available : bool = True

class RoomScheduleUpdate(RoomScheduleBase):
    pass

