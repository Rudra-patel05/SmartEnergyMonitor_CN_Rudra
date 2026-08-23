import json
import os
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models

# Ensure tables are created
models.Base.metadata.create_all(bind=engine)

def import_data():
    json_path = Path(__file__).resolve().parent.parent / 'iot' / 'data' / 'energy_readings.json'
    
    if not json_path.exists():
        print(f"Error: {json_path} not found. Please run the simulator first.")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    readings = data.get('readings', [])
    if not readings:
        print("No readings found in JSON file.")
        return
        
    db: Session = SessionLocal()
    
    # Check if data already exists to prevent duplicate imports
    existing_count = db.query(models.EnergyReading).count()
    if existing_count > 0:
        print(f"Database already contains {existing_count} records. Skipping import.")
        db.close()
        return

    # Convert and add all readings
    db_readings = []
    for r in readings:
        db_readings.append(
            models.EnergyReading(
                device_id=r['device_id'],
                area=r['area'],
                timestamp=r['timestamp'],
                voltage=r['voltage'],
                current=r['current'],
                power=r['power'],
                energy=r['energy'],
                temperature=r['temperature'],
                occupancy=r['occupancy']
            )
        )
        
    try:
        db.add_all(db_readings)
        db.commit()
        print(f"Successfully imported {len(db_readings)} records into energy.db.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting data import...")
    import_data()
