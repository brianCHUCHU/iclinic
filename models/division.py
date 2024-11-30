from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base

class Division(Base):
    __tablename__ = "division"

    # Columns
    divid = Column(String(3), primary_key=True)  # Division ID
    divname = Column(String(20), nullable=False, unique=True)  # Division Name

    # Valid division names (as per domain)
    valid_divnames = [
        '家庭醫學科', '內科', '外科', '兒科', '婦產科', '骨科', '神經科', '神經外科', '泌尿科', 
        '耳鼻喉科', '眼科', '皮膚科', '精神科', '復健科', '麻醉科', '放射診斷科', '放射腫瘤科', 
        '解剖病理科', '臨床病理科', '核子醫學科', '急診醫學科', '整形外科', '職業醫學科', 
        '西醫一般科', '牙醫一般科', '口腔病理科', '口腔顎面外科', '齒顎矯正科', '牙周病科', 
        '兒童牙科', '牙髓病科', '復補綴牙科', '牙體復形科', '家庭牙醫科', '特殊需求者口腔醫學科', 
        '中醫一般科', '中醫內科', '中醫外科', '中醫眼科', '中醫兒科', '中醫婦科', '中醫傷科', 
        '中醫針灸科', '中醫痔科'
    ]

    # # Relationships (if necessary)
    # # Example:
    # treatments = relationship("Treatment", back_populates="division")
