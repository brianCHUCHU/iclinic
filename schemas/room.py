from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel

class RoomBase(BaseModel):
    rid : str
    cid : str
    rname : str
    available : bool

class RoomCreate(RoomBase):
    rname : str = None
    available : bool = True

class RoomUpdate(RoomBase):
    rname : str = None
    available : bool = None
