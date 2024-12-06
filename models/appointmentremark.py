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

    # Relationships
    patient = relationship("Patient", back_populates="appointmentremarks")
    schedule = relationship("Schedule", back_populates="appointmentremarks")

    # 修改與 Appointment 的關聯，並顯式指定 foreign_keys
    appointment = relationship(
        "Appointment",
        back_populates="remarks",
        foreign_keys="[AppointmentRemark.pid, AppointmentRemark.sid, AppointmentRemark.date, AppointmentRemark.order]",
        primaryjoin="and_(AppointmentRemark.pid == Appointment.pid, "
                    "AppointmentRemark.sid == Appointment.sid, "
                    "AppointmentRemark.date == Appointment.date, "
                    "AppointmentRemark.order == Appointment.order)",
        cascade="all, delete-orphan"
    )
