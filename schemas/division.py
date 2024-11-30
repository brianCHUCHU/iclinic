# models/division.py

from pydantic import BaseModel

class DivisionCreate(BaseModel):
    divid: str  # For creation only
    divname: str  # The name of the division
