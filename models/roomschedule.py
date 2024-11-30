from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class RoomSchedule(Base):
    __tablename__ = "roomschedule"

    # Columns
    sid = Column(String(20), ForeignKey("schedule.sid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Schedule ID
    rid = Column(String(10), ForeignKey("room.rid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Room ID
    cid = Column(String(10), ForeignKey("clinic.cid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Clinic ID
    available = Column(Boolean, nullable=False)  # Availability status (1 for Available, 0 for Not Available)

    # Relationships (if necessary)
    # Example:
    schedule = relationship("Schedule", back_populates="roomschedules")
    room = relationship("Room", back_populates="roomschedules")
    clinic = relationship("Clinic", back_populates="roomschedules")
