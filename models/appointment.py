from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Appointment(Base):
    __tablename__ = "appointment"

    # Columns
    pid = Column(String(10), ForeignKey("patient.pid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Patient ID
    sid = Column(String(20), ForeignKey("schedule.sid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)  # Schedule ID
    date = Column(String(10), primary_key=True)  # Date of Attendance
    order = Column(Integer, primary_key=True)  # Order of the Appointment
    applytime = Column(TIMESTAMP, nullable=False)  # Datetime Applied
    status = Column(String(1), nullable=False)  # Status ('P' for pending, 'R' for rejected, 'C' for cancelled, 'O' for on-site application)
    attendance = Column(Boolean, nullable=False)  # Attendance status (1 for attended, 0 for not attended)

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    schedule = relationship("Schedule", back_populates="appointments")

    # 修改 remarks 關聯，顯式指定 foreign_keys 和 primaryjoin
    remarks = relationship(
        "AppointmentRemark",
        back_populates="appointment",
        foreign_keys="[AppointmentRemark.pid, AppointmentRemark.sid, AppointmentRemark.date, AppointmentRemark.order]",
        primaryjoin="and_(Appointment.pid == AppointmentRemark.pid, "
                    "Appointment.sid == AppointmentRemark.sid, "
                    "Appointment.date == AppointmentRemark.date, "
                    "Appointment.order == AppointmentRemark.order)",
        cascade="all, delete-orphan"
    )
