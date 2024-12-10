from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class TreatmentBase(BaseModel):
    tid : str
    docid : str
    divid : str
    cid : str
    tname: str
    available : bool

class TreatmentCreate(TreatmentBase):
    available : bool = True

class TreatmentUpdate(TreatmentBase):
    tid : str
    docid : str = None
    divid : str = None
    cid : str = None
    tname : str = None
    available : bool = None