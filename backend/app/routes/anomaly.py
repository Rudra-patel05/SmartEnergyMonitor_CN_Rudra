from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from .. import models
from ..schemas import AnomalyCheckRequest, AnomalyResponse
from ..services.anomaly_service import anomaly_service

router = APIRouter(
    prefix="/api/anomaly",
    tags=["Anomaly Detection"]
)

@router.post("/check", response_model=AnomalyResponse)
def check_anomaly(request: AnomalyCheckRequest, db: Session = Depends(get_db)):
    """
    Checks if a given telemetry reading is anomalous.
    Uses the in-memory trained Isolation Forest model.
    """
    if not anomaly_service.is_ready:
        raise HTTPException(status_code=503, detail="Anomaly service is not ready or model is not loaded.")

    # Get recent history for this device to calculate rolling features
    history = db.query(models.EnergyReading).filter(
        models.EnergyReading.device_id == request.device_id
    ).order_by(models.EnergyReading.timestamp.desc()).limit(3).all()
    
    # Convert ORM objects to dicts for the service
    history_dicts = []
    for h in history:
        history_dicts.append({
            "energy": h.energy,
            "power": h.power
        })
        
    current_reading_dict = request.dict()
    
    # Calculate features required by Isolation Forest
    features = anomaly_service.calculate_features(current_reading_dict, history_dicts)
    
    # Predict anomaly
    try:
        anomaly_flag, anomaly_score = anomaly_service.check_anomaly(features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
        
    return AnomalyResponse(
        device_id=request.device_id,
        area=request.area,
        timestamp=request.timestamp,
        anomaly_flag=anomaly_flag,
        anomaly_score=anomaly_score,
        status="ANOMALY" if anomaly_flag == 1 else "NORMAL"
    )

@router.get("/latest", response_model=List[AnomalyResponse])
def get_latest_anomalies(db: Session = Depends(get_db)):
    """
    Retrieves the latest anomaly status for all known devices.
    (Computed on request based on the latest database reading).
    """
    if not anomaly_service.is_ready:
        raise HTTPException(status_code=503, detail="Anomaly service is not ready or model is not loaded.")
        
    # Get distinct devices
    devices = db.query(models.EnergyReading.device_id).distinct().all()
    devices = [d[0] for d in devices]
    
    responses = []
    for device_id in devices:
        # Get latest reading and up to 3 previous for history
        readings = db.query(models.EnergyReading).filter(
            models.EnergyReading.device_id == device_id
        ).order_by(models.EnergyReading.timestamp.desc()).limit(4).all()
        
        if not readings:
            continue
            
        latest = readings[0]
        history = readings[1:]
        
        current_reading_dict = {
            "device_id": latest.device_id,
            "area": latest.area,
            "timestamp": latest.timestamp.strftime("%Y-%m-%d %H:%M:%S") if isinstance(latest.timestamp, datetime) else latest.timestamp,
            "voltage": latest.voltage,
            "current": latest.current,
            "power": latest.power,
            "energy": latest.energy,
            "temperature": latest.temperature,
            "occupancy": latest.occupancy,
        }
        
        history_dicts = [{"energy": h.energy, "power": h.power} for h in history]
        
        features = anomaly_service.calculate_features(current_reading_dict, history_dicts)
        
        try:
            flag, score = anomaly_service.check_anomaly(features)
            responses.append(
                AnomalyResponse(
                    device_id=latest.device_id,
                    area=latest.area,
                    timestamp=current_reading_dict["timestamp"],
                    anomaly_flag=flag,
                    anomaly_score=score,
                    status="ANOMALY" if flag == 1 else "NORMAL"
                )
            )
        except Exception:
            pass # skip if error
            
    return responses
