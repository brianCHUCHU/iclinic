from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class AppointmentRemark(Base):
    __tablename__ = "appointmentremark"

    # Columns
    pid = Column(String(10), ForeignKey("patient.pid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Patient ID
    sid = Column(String(20), ForeignKey("schedule.sid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Schedule ID
    date = Column(Date, ForeignKey("appointment.date", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Date of Attendance
    order = Column(Integer, ForeignKey("appointment.order", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Order of the Appointment
    text = Column(String(4000), nullable=False)  # Content of the Remark
    datetime = Column(TIMESTAMP, primary_key=True, nullable=False)  # Datetime of Remark Commented

    # Relationships (if necessary, based on other models)
    # Example:
    patient = relationship("Patient", back_populates="appointmentremarks")
    schedule = relationship("Schedule", back_populates="appointmentremarks")
    appointment = relationship("Appointment", back_populates="appointmentremarks")
