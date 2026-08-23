"""
Configuration for the Virtual IoT Energy Meter Simulator.

All IoT devices are SIMULATED. No physical sensors or hardware are used.
This configuration defines campus areas, device parameters, and simulation defaults.
"""

import os
from pathlib import Path
from typing import Dict, List, Any

# ============================================================
# Directory Paths
# ============================================================
# Resolve paths relative to this file's location (iot/ directory)
BASE_DIR: str = str(Path(__file__).resolve().parent)
DATA_DIR: str = str(Path(BASE_DIR) / "data")
CSV_OUTPUT_PATH: str = str(Path(DATA_DIR) / "energy_readings.csv")
JSON_OUTPUT_PATH: str = str(Path(DATA_DIR) / "energy_readings.json")

# ============================================================
# Simulation Defaults
# ============================================================
DEFAULT_READINGS_PER_DEVICE: int = 100
DEFAULT_INTERVAL_SECONDS: int = 900  # 15 minutes between readings

# ============================================================
# Electrical System (Indian Standard)
# ============================================================
NOMINAL_VOLTAGE: float = 230.0   # Standard voltage in India (Volts)
VOLTAGE_VARIATION: float = 5.0   # Typical variation ±5V

# ============================================================
# Campus Area Device Configurations
# ============================================================
# Each device represents a virtual smart energy meter installed
# in a specific campus area. The configuration controls how
# realistic the simulated data will be.
#
# Fields:
#   device_id        : Unique identifier for the virtual meter
#   area             : Human-readable campus area name
#   operating_hours  : (start_hour, end_hour) when the area is open
#   peak_hours       : (start_hour, end_hour) for highest activity
#   max_occupancy    : Maximum number of people in the area
#   base_current     : Standby current draw in Amperes (lights off, minimal load)
#   peak_current     : Maximum current draw in Amperes (full load)
#   temp_range       : (min_temp, max_temp) in Celsius for the area
#   temp_occupied_boost : Extra temperature rise (°C) when area is fully occupied

DEVICE_CONFIGS: List[Dict[str, Any]] = [
    {
        "device_id": "LAB-01",
        "area": "Computer Laboratory 1",
        "operating_hours": (8, 18),   # 8:00 AM – 6:00 PM
        "peak_hours": (9, 17),        # 9:00 AM – 5:00 PM
        "max_occupancy": 40,
        "base_current": 2.0,          # Standby: emergency lights, server standby
        "peak_current": 25.0,         # Full load: 40 PCs + AC + monitors
        "temp_range": (22.0, 28.0),
        "temp_occupied_boost": 3.0,   # PCs + people generate significant heat
    },
    {
        "device_id": "LAB-02",
        "area": "Computer Laboratory 2",
        "operating_hours": (8, 18),
        "peak_hours": (9, 17),
        "max_occupancy": 35,
        "base_current": 2.0,
        "peak_current": 22.0,         # Slightly smaller lab
        "temp_range": (22.0, 28.0),
        "temp_occupied_boost": 2.5,
    },
    {
        "device_id": "CLASS-01",
        "area": "Classroom 1",
        "operating_hours": (8, 16),   # 8:00 AM – 4:00 PM
        "peak_hours": (9, 15),        # 9:00 AM – 3:00 PM
        "max_occupancy": 60,
        "base_current": 1.0,          # Standby: minimal
        "peak_current": 12.0,         # Lights + fans + projector + AC
        "temp_range": (24.0, 32.0),   # Classrooms can get warm
        "temp_occupied_boost": 2.0,
    },
    {
        "device_id": "LIB-01",
        "area": "Library",
        "operating_hours": (9, 20),   # 9:00 AM – 8:00 PM (longer hours)
        "peak_hours": (10, 18),       # 10:00 AM – 6:00 PM
        "max_occupancy": 50,
        "base_current": 2.0,          # Standby: security systems
        "peak_current": 15.0,         # Lights + AC + computers + charging
        "temp_range": (22.0, 26.0),   # Libraries maintain cooler temp
        "temp_occupied_boost": 1.5,
    },
    {
        "device_id": "ADMIN-01",
        "area": "Administrative Office",
        "operating_hours": (9, 18),   # 9:00 AM – 6:00 PM
        "peak_hours": (10, 17),       # 10:00 AM – 5:00 PM
        "max_occupancy": 15,
        "base_current": 1.5,          # Standby: server, security
        "peak_current": 10.0,         # PCs + printers + AC + lights
        "temp_range": (23.0, 28.0),
        "temp_occupied_boost": 1.0,   # Fewer people, less heat
    },
]
