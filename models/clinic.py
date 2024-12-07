from sqlalchemy import Column, Integer, String, CHAR
from sqlalchemy.orm import relationship
from .room import Room
from .doctor import Hire
from .base import Base

class Clinic(Base):
    __tablename__ = "clinic"

    # Columns
    cid = Column(String(10), primary_key=True)  # Clinic ID
    fee = Column(Integer, nullable=False)  # Clinic Appointment Fee
    queue_type = Column(String(1), nullable=False)  # 'S' or 'I'
    acct_name = Column(String(30), nullable=False)  # Clinic Account Name
    acct_pw = Column(String(100), nullable=False)  # Clinic Password
    cname = Column(String(30), nullable=False)  # Clinic Name
    city = Column(String(50), nullable=False)  # Clinic City
    district = Column(String(50), nullable=False)  # Clinic District
    address = Column(String(100), nullable=False)  # Clinic Address (excluding city and district)
    available = Column(String(1), nullable=False)


    # Relationships
    rooms = relationship("Room", cascade="all, delete, save-update")
    hires = relationship("Hire", cascade="all, delete, save-update")
    treatments = relationship("Treatment" ,cascade="all, delete, save-update")
    periods = relationship("Period" ,cascade="all, delete, save-update")
