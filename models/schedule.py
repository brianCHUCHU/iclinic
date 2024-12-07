from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Schedule(Base):
    __tablename__ = "schedule"

    sid = Column(String(20), primary_key=True)  # Schedule ID
    divid = Column(String(3), ForeignKey("division.divid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)  # Division ID
    perid = Column(String(10), ForeignKey("period.perid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)  # Period ID
    docid = Column(String(10), ForeignKey("doctor.docid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)  # Doctor ID
    available = Column(String(1), nullable=False)  # Schedule availability status

    division = relationship("Division", back_populates="schedules")
    period = relationship("Period", back_populates="schedules")
    doctor = relationship("Doctor", back_populates="schedules")
