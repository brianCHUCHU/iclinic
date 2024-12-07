from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Treatment(Base):
    __tablename__ = "treatment"

    # Columns
    tid = Column(String(20), primary_key=True)  # Treatment ID
    docid = Column(String(10), ForeignKey("doctor.docid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)  # Doctor ID
    divid = Column(String(3), ForeignKey("division.divid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)  # Division ID
    cid = Column(String(10), ForeignKey("clinic.cid", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)  # Clinic ID
    tname = Column(String(20), nullable=False)  # Treatment Name
    available = Column(String(1), nullable=False)

    # # Relationships (if necessary)
    # # Example:
    # doctor = relationship("Doctor", back_populates="treatments")
    # division = relationship("Division", back_populates="treatments")
    # clinic = relationship("Clinic", back_populates="treatments")
