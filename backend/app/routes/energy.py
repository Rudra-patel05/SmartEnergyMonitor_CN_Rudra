from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/api/energy",
    tags=["energy"]
)

@router.post("/readings", response_model=schemas.EnergyReading, status_code=201)
def create_reading(reading: schemas.EnergyReadingCreate, db: Session = Depends(get_db)):
    """
    Store a single energy reading.
    """
    db_reading = models.EnergyReading(**reading.model_dump())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

@router.post("/readings/bulk", response_model=List[schemas.EnergyReading], status_code=201)
def create_bulk_readings(readings: List[schemas.EnergyReadingCreate], db: Session = Depends(get_db)):
    """
    Store multiple energy readings in bulk.
    """
    db_readings = [models.EnergyReading(**r.model_dump()) for r in readings]
    db.add_all(db_readings)
    db.commit()
    
    # Return added objects (refresh is tricky for bulk, so we just return the in-memory states)
    return db_readings

@router.get("/readings", response_model=List[schemas.EnergyReading])
def get_readings(
    device_id: Optional[str] = None,
    area: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Retrieve energy readings with optional filtering.
    """
    query = db.query(models.EnergyReading)
    
    if device_id:
        query = query.filter(models.EnergyReading.device_id == device_id)
    if area:
        query = query.filter(models.EnergyReading.area.contains(area))
        
    # Order by timestamp descending (most recent first)
    return query.order_by(models.EnergyReading.timestamp.desc()).limit(limit).all()

@router.get("/summary", response_model=schemas.EnergySummary)
def get_summary(db: Session = Depends(get_db)):
    """
    Get aggregated summary statistics of all readings.
    """
    total = db.query(models.EnergyReading).count()
    if total == 0:
        return schemas.EnergySummary(
            total_readings=0,
            average_power=0.0,
            average_energy=0.0,
            max_power=0.0,
            total_energy=0.0
        )
        
    avg_power = db.query(func.avg(models.EnergyReading.power)).scalar() or 0.0
    avg_energy = db.query(func.avg(models.EnergyReading.energy)).scalar() or 0.0
    max_power = db.query(func.max(models.EnergyReading.power)).scalar() or 0.0
    
    # Total energy is sum of max energy per device
    subq = db.query(
        models.EnergyReading.device_id,
        func.max(models.EnergyReading.energy).label('max_energy')
    ).group_by(models.EnergyReading.device_id).subquery()
    
    total_energy = db.query(func.sum(subq.c.max_energy)).scalar() or 0.0

    return schemas.EnergySummary(
        total_readings=total,
        average_power=round(avg_power, 2),
        average_energy=round(avg_energy, 4),
        max_power=round(max_power, 2),
        total_energy=round(total_energy, 4)
    )

@router.get("/{device_id}", response_model=List[schemas.EnergyReading])
def get_device_readings(device_id: str, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get readings for a specific device.
    """
    readings = db.query(models.EnergyReading).filter(
        models.EnergyReading.device_id == device_id
    ).order_by(models.EnergyReading.timestamp.desc()).limit(limit).all()
    
    if not readings:
        raise HTTPException(status_code=404, detail="Device not found or no readings available")
    return readings
