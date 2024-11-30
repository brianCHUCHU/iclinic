from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Hire(Base):
    __tablename__ = "hire"

    # Columns
    docid = Column(String(10), ForeignKey("doctor.docid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Doctor ID
    cid = Column(String(10), ForeignKey("clinic.cid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Clinic ID
    divid = Column(String(10), ForeignKey("division.divid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Division ID
    startdate = Column(Date, nullable=True)  # Start Date of Hiring
    enddate = Column(Date, nullable=True)  # End Date of Hiring

    # Relationships (if necessary)
    # Example:
    doctor = relationship("Doctor", back_populates="hires")
    clinic = relationship("Clinic", back_populates="hires")
    division = relationship("Division", back_populates="hires")
