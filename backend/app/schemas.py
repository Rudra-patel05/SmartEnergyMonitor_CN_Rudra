from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class EnergyReadingBase(BaseModel):
    device_id: str = Field(..., description="Unique identifier for the device", min_length=3)
    area: str = Field(..., description="Campus area name")
    timestamp: str = Field(..., description="Timestamp of the reading in YYYY-MM-DD HH:MM:SS format")
    voltage: float = Field(..., gt=0, description="Voltage in Volts")
    current: float = Field(..., ge=0, description="Current in Amperes")
    power: float = Field(..., ge=0, description="Power in Watts")
    energy: float = Field(..., ge=0, description="Cumulative energy in kWh")
    temperature: float = Field(..., ge=-20.0, le=60.0, description="Temperature in Celsius")
    occupancy: int = Field(..., ge=0, description="Occupancy count")

    @validator('device_id')
    def validate_device_id(cls, v):
        valid_prefixes = ['LAB', 'CLASS', 'LIB', 'ADMIN']
        if not any(v.startswith(prefix) for prefix in valid_prefixes):
            raise ValueError("device_id must start with LAB, CLASS, LIB, or ADMIN")
        return v

    @validator('timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            return v
        except ValueError:
            raise ValueError("Timestamp must be in YYYY-MM-DD HH:MM:SS format")

class EnergyReadingCreate(EnergyReadingBase):
    pass

class EnergyReading(EnergyReadingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class EnergySummary(BaseModel):
    total_readings: int
    average_power: float
    average_energy: float
    max_power: float
    total_energy: float
