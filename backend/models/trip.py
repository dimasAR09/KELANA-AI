from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, nullable=False)
    days = Column(Integer, nullable=False)
    budget = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    daily_budget = Column(Float, nullable=False)
    travel_style = Column(String, nullable=True)
    ai_recommendation = Column(Text, nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="trips")

class DestinationDB(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, index=True)
    kota = Column(String)
    kondisi_cuaca = Column(String) 
    ramah_anak = Column(Boolean)
    kategori_biaya = Column(String)