from sqlalchemy import Column, String, Integer, ForeignKey, Time, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Period(Base):
    __tablename__ = "period"

    perid = Column(String(20), primary_key=True)  # Period ID
    cid = Column(String(10), ForeignKey("clinic.cid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)  # Foreign Key: Clinic ID
    weekday = Column(Integer, nullable=False)  # Weekday (1~7)
    starttime = Column(Time, nullable=False)  # Start Time
    endtime = Column(Time, nullable=False)  # End Time
    available = Column(Boolean, nullable=False)  # Availability Status: 1 (True), 0 (False)

    # Relationships (optional)
    clinic = relationship("Clinic", back_populates="periods")
