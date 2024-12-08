from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel

class ClinicDivisionBase(BaseModel):
    divid: str
    cid: str

class ClinicDivisionCreate(ClinicDivisionBase):
    available : bool = True

class ClinicDivisionUpdate(ClinicDivisionBase):
    pass