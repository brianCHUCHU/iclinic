from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel

class RoomBase(BaseModel):
    rid : str
    cid : str
    rname : str
    available : str

class RoomCreate(RoomBase):
    rname : str = None
    available : str = "1"

class RoomUpdate(RoomBase):
    pass
