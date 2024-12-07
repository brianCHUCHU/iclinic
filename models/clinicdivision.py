from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ClinicDivision(Base):
    __tablename__ = "clinicdivision"

    # Columns
    divid = Column(String(3), ForeignKey("division.divid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Division ID
    cid = Column(String(10), ForeignKey("clinic.cid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Clinic ID
    available = Column(String(1), nullable=False)

    # Relationships (if necessary)
    # Example:
    division = relationship("Division", back_populates="clinicdivisions")
    clinic = relationship("Clinic", back_populates="clinicdivisions")
