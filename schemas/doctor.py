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

