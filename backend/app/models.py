from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class EnergyReading(Base):
    __tablename__ = "energy_readings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(String, index=True, nullable=False)
    area = Column(String, index=True, nullable=False)
    timestamp = Column(String, nullable=False)  # We store as ISO 8601 string from simulator
    voltage = Column(Float, nullable=False)
    current = Column(Float, nullable=False)
    power = Column(Float, nullable=False)
    energy = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    occupancy = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
