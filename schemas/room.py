from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
# import pydantic datetime
import datetime

class RoomBase(BaseModel):
    rid : str
    cid : str
    rname : str
    available : bool

class RoomCreate(BaseModel):
    rname : str
    cid : str
    available : bool = True

class RoomUpdate(BaseModel):
    rid: str
    rname: Optional[str]

class RoomUpdateQueue(BaseModel):
    rid: str
    queuenumber: int
    lastupdate: datetime.datetime