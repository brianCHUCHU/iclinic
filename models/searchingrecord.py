from sqlalchemy import Column, String, Decimal, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class SearchingRecord(Base):
    __tablename__ = "searchingrecord"

    # Columns
    pid = Column(String(10), ForeignKey("patient.pid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)  # Patient ID
    recordid = Column(String(20), primary_key=True, nullable=False)  # Record ID
    keyword = Column(String(30))  # Keyword
    plat = Column(Decimal(8, 6))  # Patient's Latitude
    plon = Column(Decimal(9, 6))  # Patient's Longitude
    divid = Column(String(3))  # Division ID
    city = Column(String(50))  # City
    district = Column(String(50))  # District

    # Relationships (if necessary)
    # Example:
    patient = relationship("Patient", back_populates="searching_records")
