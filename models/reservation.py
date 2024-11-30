from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Reservation(Base):
    __tablename__ = "reservation"

    # Columns
    pid = Column(String(10), ForeignKey("patient.pid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Patient ID
    sid = Column(String(20), ForeignKey("schedule.sid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Schedule ID
    date = Column(String(10), primary_key=True)  # Date of Attendance
    applytime = Column(TIMESTAMP, nullable=False)  # Datetime Applied
    tid = Column(String(20), ForeignKey("treatment.tid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)  # Treatment ID
    status = Column(String(1), nullable=False)  # Status ('P' for pending, 'R' for rejected, 'C' for cancelled, 'O' for on-site application)
    attendance = Column(Boolean, nullable=False)  # Attendance status (1 for attended, 0 for not attended)

    # Relationships (if necessary)
    # Example:
    patient = relationship("Patient", back_populates="reservations")
    schedule = relationship("Schedule", back_populates="reservations")
    treatment = relationship("Treatment", back_populates="reservations")