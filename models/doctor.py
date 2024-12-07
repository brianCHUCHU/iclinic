from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Doctor(Base):
    __tablename__ = "doctor"

    # Columns
    docid = Column(String(10), primary_key=True)  # Doctor ID
    docname = Column(String(20), nullable=False)  # Doctor Name

    # Relationships (if necessary)
    hires = relationship("Hire", cascade="all, delete, save-update")
    treatments = relationship("Treatment" ,cascade="all, delete, save-update")
    schedules = relationship("Schedule" ,cascade="all, delete, save-update")

class Hire(Base):
    __tablename__ = "hire"

    # Columns
    docid = Column(String(10), ForeignKey("doctor.docid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Doctor ID
    cid = Column(String(10), ForeignKey("clinic.cid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Clinic ID
    divid = Column(String(10), ForeignKey("division.divid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Division ID
    startdate = Column(Date, nullable=True)  # Start Date of Hiring
    enddate = Column(Date, nullable=True)  # End Date of Hiring
