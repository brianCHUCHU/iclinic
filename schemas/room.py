from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel

class RoomBase(BaseModel):
    rid : str
    cid : str
    rname : str

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    rid: str
    rname: str
    cid: Optional[str]

