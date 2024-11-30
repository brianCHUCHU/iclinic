from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base

class Doctor(Base):
    __tablename__ = "doctor"

    # Columns
    docid = Column(String(10), primary_key=True)  # Doctor ID
    docname = Column(String(20), nullable=False)  # Doctor Name

    # Relationships (if necessary)
    # Example:
    hires = relationship("Hire", back_populates="doctor", cascade="all, delete, save-update")
