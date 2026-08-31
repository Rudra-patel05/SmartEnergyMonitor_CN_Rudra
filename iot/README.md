# IoT Simulator Module

> Virtual IoT Energy Meter Simulator for the Smart Energy Monitoring System

---

## What is a Virtual IoT Meter?

A **Virtual IoT Meter** is a Python-based software simulation of a physical smart energy meter. Instead of reading actual electrical measurements from hardware sensors, the simulator **generates realistic energy consumption data** using mathematical models and randomization.

Each virtual meter represents a smart energy monitoring device that would be installed in a campus area in a real deployment.

---

## Why Use Simulation?

| Reason | Explanation |
|--------|-------------|
| **No hardware cost** | The prototype works without purchasing physical sensors, microcontrollers, or wiring |
| **Rapid development** | Data is available instantly — no need to wait for hardware setup or real-time collection |
| **Controlled testing** | We can generate specific scenarios (peak hours, anomalies, weekends) on demand |
| **Reproducibility** | The same simulation can be run multiple times for consistent testing |
| **Academic focus** | The project focuses on AI, networking, and software architecture — not electronics |
| **Future-ready** | The system architecture allows replacing the simulator with real sensors later |

> **Important:** All IoT data in this project is SIMULATED. No physical sensors or hardware are deployed.

---

## Campus Areas Monitored

| Device ID | Area | Max Occupancy | Operating Hours |
|-----------|------|:------------:|:---------------:|
| **LAB-01** | Computer Laboratory 1 | 40 | 08:00 – 18:00 |
| **LAB-02** | Computer Laboratory 2 | 35 | 08:00 – 18:00 |
| **CLASS-01** | Classroom 1 | 60 | 08:00 – 16:00 |
| **LIB-01** | Library | 50 | 09:00 – 20:00 |
| **ADMIN-01** | Administrative Office | 15 | 09:00 – 18:00 |

---

## Data Fields

Each energy reading contains the following fields:

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `device_id` | String | — | Unique identifier for the virtual meter (e.g., `LAB-01`) |
| `area` | String | — | Human-readable campus area name |
| `timestamp` | String | YYYY-MM-DD HH:MM:SS | Time when the reading was taken |
| `voltage` | Float | Volts (V) | Simulated voltage (~230V ± variation) |
| `current` | Float | Amperes (A) | Simulated current draw based on load |
| `power` | Float | Watts (W) | Calculated: `voltage × current` |
| `energy` | Float | Kilowatt-hours (kWh) | Cumulative energy consumed |
| `temperature` | Float | Celsius (°C) | Simulated room temperature |
| `occupancy` | Integer | People | Simulated number of people in the area |

---

## How the Simulator Works

### Simulation Logic

1. **Occupancy** is determined by:
   - Time of day (operating hours vs. closed)
   - Day of week (weekday vs. weekend)
   - Area type (lab, classroom, library, office)
   - Random variation for realism

2. **Current** is calculated based on:
   - Occupancy level (more people → more devices → higher current)
   - Base current (standby load when area is closed)
   - Peak current (full load when area is at capacity)
   - ±10% random noise

3. **Voltage** is simulated around 230V (Indian standard) with Gaussian noise.

4. **Power** is calculated as:
   ```
   power_watts = voltage × current
   ```

5. **Energy** is calculated as:
   ```
   energy_kwh = power_watts × (interval_seconds / 3600) / 1000
   ```
   Energy is accumulated over the simulation run.

6. **Temperature** depends on:
   - Base temperature range for the area
   - Time of day (warmer in afternoon)
   - Occupancy (more people → more body heat)

### Realistic Patterns

| Area | Pattern |
|------|---------|
| Computer Labs | High consumption during 9–5 (PCs + AC), very low at night |
| Classroom | Moderate during class hours (8–4), zero when empty |
| Library | Steady moderate load during long hours (9–8 PM) |
| Admin Office | Moderate during office hours (9–6), low standby at night |

---

## How to Run

### Prerequisites

- Python 3.11 or later
- No external packages required (uses only Python standard library)

### Basic Run (100 readings per device)

```bash
python iot/simulator.py
```

### Custom Number of Readings

```bash
python iot/simulator.py --readings 200
```

### Custom Interval (in seconds)

```bash
python iot/simulator.py --readings 50 --interval 600
```

### Send Data to Backend API

By default, the simulator only saves to local files. To automatically send the generated readings to the FastAPI backend via HTTP POST, use the `--send-api` flag. The default backend URL is `http://127.0.0.1:8000`.

```bash
python iot/simulator.py --readings 20 --send-api
```

You can optionally override the backend URL:

```bash
python iot/simulator.py --send-api --api-url http://192.168.1.100:8000
```

#### Example Output (API Sending)
```text
  Total readings generated : 100
  Validation errors        : 0

  Sending 100 readings to API at http://127.0.0.1:8000...
    Sent: 100
    Successful: 100
    Failed: 0
```

### Help

```bash
python iot/simulator.py --help
```

---

## Output Files

| File | Format | Path |
|------|--------|------|
| CSV | Comma-separated values | `iot/data/energy_readings.csv` |
| JSON | JSON with metadata | `iot/data/energy_readings.json` |

### CSV Format

```csv
device_id,area,timestamp,voltage,current,power,energy,temperature,occupancy
LAB-01,Computer Laboratory 1,2026-08-22 09:15:00,231.2,18.45,4265.64,1.0664,24.8,32
LAB-01,Computer Laboratory 1,2026-08-22 09:30:00,229.8,19.12,4394.18,2.1649,25.1,35
```

### JSON Format

```json
{
  "metadata": {
    "project": "Smart Energy Monitor – Smart Campus",
    "description": "Simulated IoT energy readings (no physical sensors)",
    "generated_at": "2026-08-23 17:30:00",
    "total_records": 500,
    "devices": ["ADMIN-01", "CLASS-01", "LAB-01", "LAB-02", "LIB-01"],
    "areas": ["Administrative Office", "Classroom 1", "Computer Laboratory 1", "Computer Laboratory 2", "Library"]
  },
  "readings": [
    {
      "device_id": "LAB-01",
      "area": "Computer Laboratory 1",
      "timestamp": "2026-08-22 09:15:00",
      "voltage": 231.2,
      "current": 18.45,
      "power": 4265.64,
      "energy": 1.0664,
      "temperature": 24.8,
      "occupancy": 32
    }
  ]
}
```

---

## File Structure

```
iot/
├── simulator.py     # Main entry point — run this script
├── devices.py       # VirtualEnergyMeter class definition
├── config.py        # Device configurations and simulation parameters
├── data/            # Generated output (created automatically)
│   ├── energy_readings.csv
│   └── energy_readings.json
└── README.md        # This file
```

---

## Device Authentication (Day 12)

Virtual IoT devices are authenticated at the FastAPI Backend Ingestion API using a pre-shared **`X-API-Key`** header:
- The key is configured via the environment variable `SMART_ENERGY_API_KEY` (falls back to a default academic key in `iot/config.py`).
- The `ApiClient` automatically appends this header to all `POST` requests.
- Requests sent without a valid key are rejected by the backend with an `HTTP 401 Unauthorized` status code.

---

## Validation

The simulator validates every generated reading:

| Check | Rule |
|-------|------|
| Voltage | Must be > 0 |
| Current | Must be ≥ 0 |
| Power | Must be ≥ 0 |
| Energy | Must be ≥ 0 |
| Occupancy | Must be ≥ 0 |
| Timestamp | Must be a valid datetime string |

Any validation errors are printed to the console during simulation.

---

*Module Version: 1.1 | Created: August 2026 | Day 12 Updated*
