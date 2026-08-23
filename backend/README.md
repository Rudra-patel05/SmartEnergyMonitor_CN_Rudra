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
