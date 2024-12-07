from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel

class TreatmentBase(BaseModel):
    tid : str
    docid : str
    divid : str
    cid : str
    tname: str
    available : str

class TreatmentCreate(TreatmentBase):
    tname: str = None
    available : str = "1"

class TreatmentUpdate(TreatmentBase):
    tname : str = None
    available : str = None