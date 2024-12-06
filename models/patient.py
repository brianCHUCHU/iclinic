from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Patient(Base):
    __tablename__ = "patient"  # 映射到已存在的表
    pid = Column(String(10), primary_key=True)
    pname = Column(String(10), nullable=False)
    birthdate = Column(Date, nullable=False)
    gender = Column(String(1), nullable=False)
    status = Column(String(1), nullable=False)

    # 關聯 Membership
    membership = relationship("Membership", back_populates="patient", uselist=False)

    # 關聯 Appointment (新增的部分)
    appointments = relationship("Appointment", back_populates="patient")
    appointmentremarks = relationship("AppointmentRemark", back_populates="patient")