from sqlalchemy import Column, String, Date, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ReservationRemark(Base):
    __tablename__ = "reservationremark"

    # Columns
    pid = Column(String(10), ForeignKey("patient.pid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Patient ID
    sid = Column(String(20), ForeignKey("schedule.sid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Schedule ID
    date = Column(Date, ForeignKey("reservation.date", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Date of Attendance
    text = Column(String(4000), nullable=False)  # Content of the Remark
    datetime = Column(TIMESTAMP, primary_key=True, nullable=False)  # Datetime of Remark Commented

    # Relationships (if necessary)
    # Example:
    patient = relationship("Patient", back_populates="reservationremarks")
    schedule = relationship("Schedule", back_populates="reservationremarks")
    reservation = relationship("Reservation", back_populates="reservationremarks")
