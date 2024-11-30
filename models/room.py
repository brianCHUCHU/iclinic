from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Room(Base):
    __tablename__ = "room"

    rid = Column(String(10), primary_key=True)
    cid = Column(String(20), ForeignKey("clinic.cid", ondelete="CASCADE"), primary_key=True)
    rname = Column(String(5), nullable=False)

    # Relationship to Clinic
    clinic = relationship("Clinic", back_populates="rooms")
