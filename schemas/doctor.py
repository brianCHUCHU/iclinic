from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel

class DoctorBase(BaseModel):
    docid : str
    docname : str

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    pass

class HireBase(BaseModel):
    docid : str
    cid : str
    divid : str
    startdate : Optional[str] = None
    enddate : Optional[str] = None

class HireCreate(HireBase):
    pass

class HireUpdate(HireBase):
    pass