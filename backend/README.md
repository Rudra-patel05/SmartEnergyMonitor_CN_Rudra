# Backend Module

> FastAPI backend server for the Smart Energy Monitoring System.

This module provides the REST API and database integration for storing and analyzing simulated IoT energy data.

## Features

- **FastAPI**: High-performance API framework
- **SQLAlchemy**: ORM for database interaction
- **SQLite**: Local file-based database (`energy.db`)
- **Pydantic**: Data validation and serialization
- **Bulk Data Loading**: Endpoint to ingest data from the simulator

## Setup and Installation

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Import existing simulator data (optional):
   ```bash
   python import_data.py
   ```
   This script will read `../iot/data/energy_readings.json` and insert it into the database via the API.

## IoT Simulator Integration

As of **Day 4**, the Virtual IoT Simulator can send data directly to the backend in real-time or in batch via HTTP POST instead of requiring the manual `import_data.py` script. 

To use this feature, ensure the FastAPI server is running, then use the simulator's `--send-api` flag:

```bash
# In the iot directory:
python simulator.py --readings 20 --send-api
```

The simulator uses the `/api/energy/readings/bulk` endpoint to efficiently transmit data.

## Running the Server

Start the API server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The server will be available at: http://127.0.0.1:8000

## API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/energy/readings` | Submit a single energy reading |
| `POST` | `/api/energy/readings/bulk` | Submit multiple readings at once |
| `GET` | `/api/energy/readings` | Retrieve readings (supports filtering by `device_id`, `area`) |
| `GET` | `/api/energy/{device_id}` | Retrieve readings for a specific device |
| `GET` | `/api/energy/summary` | Get aggregated summary statistics |
| `POST` | `/api/prediction/energy/predict` | Predict next energy for a device using XGBoost (Day 9) |
| `GET` | `/api/prediction/energy/predictions/latest` | Get latest predictions for all devices (Day 9) |

## Example Request (Single Reading)

**POST `/api/energy/readings`**
```json
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
```

## Example Response
```json
{
  "device_id": "LAB-01",
  "area": "Computer Laboratory 1",
  "timestamp": "2026-08-22 09:15:00",
  "voltage": 231.2,
  "current": 18.45,
  "power": 4265.64,
  "energy": 1.0664,
  "temperature": 24.8,
  "occupancy": 32,
  "id": 1,
  "created_at": "2026-08-23T12:00:00.000000"
}
```
