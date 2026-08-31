from pydantic import BaseModel, Field, validator
from typing import Optional, List
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


# ---------------------------------------------------------------------------
# Day 9 — Prediction schemas
# ---------------------------------------------------------------------------

class PredictionRequest(BaseModel):
    """Request body for POST /api/prediction/energy/predict."""
    device_id: str = Field(
        ...,
        description="Device ID to predict next energy for (e.g. LAB001)",
        min_length=3,
    )


class PredictionResponse(BaseModel):
    """Response from the XGBoost energy prediction endpoint."""
    device_id: str = Field(..., description="Device identifier")
    area: str = Field(..., description="Campus area of the device")
    timestamp: str = Field(..., description="Timestamp when prediction was generated (UTC)")
    predicted_next_energy: float = Field(
        ..., description="Predicted next cumulative energy reading in kWh"
    )
    model_name: str = Field(..., description="Name of the ML model used (XGBoost)")

# ---------------------------------------------------------------------------
# Day 10 — Anomaly detection schemas
# ---------------------------------------------------------------------------

class AnomalyCheckRequest(EnergyReadingBase):
    """Request body for POST /api/anomaly/check."""
    pass


class AnomalyResponse(BaseModel):
    """Response from the anomaly detection endpoint."""
    device_id: str = Field(..., description="Device identifier")
    area: str = Field(..., description="Campus area of the device")
    timestamp: str = Field(..., description="Timestamp of the reading")
    anomaly_flag: int = Field(..., description="1 if anomaly detected, 0 if normal")
    anomaly_score: float = Field(..., description="Anomaly score from Isolation Forest")
    status: str = Field(..., description="'ANOMALY' or 'NORMAL'")

# ---------------------------------------------------------------------------
# Day 12 — Authentication & Cybersecurity schemas
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    """Credentials payload for JWT authentication."""
    username: str = Field(..., min_length=3, max_length=50, description="User username")
    password: str = Field(..., min_length=6, description="User password")


class TokenResponse(BaseModel):
    """JWT Token issuance response."""
    access_token: str = Field(..., description="Signed JSON Web Token")
    token_type: str = Field("bearer", description="Token type")
    expires_in_minutes: int = Field(..., description="Token validity window in minutes")
    role: str = Field(..., description="User role (admin, operator)")
    username: str = Field(..., description="Authenticated username")


class AuthStatusResponse(BaseModel):
    """Current authentication and security system status."""
    status: str
    auth_mode: str
    jwt_algorithm: str
    device_auth_enabled: bool
    active_users: List[str]
