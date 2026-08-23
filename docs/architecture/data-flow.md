# Data Flow Architecture

> End-to-End Data Flow for the Smart Energy Monitoring System

---

## 1. Overview

This document traces the complete journey of energy data from its origin at the virtual IoT meters through the network, backend, database, AI engine, and finally to the web dashboard for visualization.

---

## 2. High-Level Data Flow

```
┌──────────────────┐
│  Virtual IoT      │
│  Energy Meter     │    Step 1: Data Generation
│  (Python Script)  │
└────────┬─────────┘
         │
         │  JSON payload via HTTP POST
         │
┌────────▼─────────┐
│  Campus Network   │    Step 2: Network Transport
│  (VLAN-segmented) │
└────────┬─────────┘
         │
         │  TCP/IP packets routed to server VLAN
         │
┌────────▼─────────┐
│  Backend API      │    Step 3: Data Ingestion
│  (FastAPI)        │
│  + JWT Auth       │
└────────┬─────────┘
         │
         │  Validated and structured data
         │
┌────────▼─────────┐
│  Database         │    Step 4: Data Persistence
│  (SQLite)         │
└────────┬─────────┘
         │
         │  Historical data query
         │
┌────────▼─────────┐
│  AI / ML Engine   │    Step 5: Data Analysis
│  (Scikit-learn)   │
│                   │
│  ┌─────────────┐  │
│  │ Prediction  │  │    Step 5a: Forecast future consumption
│  └─────────────┘  │
│  ┌─────────────┐  │
│  │ Anomaly     │  │    Step 5b: Detect unusual patterns
│  │ Detection   │  │
│  └─────────────┘  │
└────────┬─────────┘
         │
         │  Prediction results + anomaly alerts
         │
┌────────▼─────────┐
│  Database         │    Step 6: Results Storage
│  (SQLite)         │
└────────┬─────────┘
         │
         │  REST API response (JSON)
         │
┌────────▼─────────┐
│  Web Dashboard    │    Step 7: Visualization
│  (React + Vite)   │
└──────────────────┘
```

---

## 3. Detailed Step-by-Step Flow

### Step 1: Data Generation (IoT Simulator)

**Component:** Python IoT Simulator Script

The virtual IoT energy meter generates simulated energy consumption data for each campus area.

**Process:**
1. The simulator script runs on a configurable interval (e.g., every 60 seconds).
2. For each campus area, it generates a reading based on:
   - Current time of day (peak vs. off-peak)
   - Day of week (weekday vs. weekend)
   - Area type (lab, classroom, library, office)
   - Random noise for realism
3. The reading is packaged as a JSON payload.

**Example Output:**
```json
{
  "area_id": "comp_lab_01",
  "area_name": "Computer Laboratory",
  "timestamp": "2026-08-23T10:30:00Z",
  "voltage": 228.5,
  "current": 12.3,
  "power": 2810.55,
  "energy": 45.67,
  "power_factor": 0.92
}
```

**Output:** JSON payload → HTTP POST request

---

### Step 2: Network Transport

**Component:** Campus Network (Simulated in Cisco Packet Tracer)

The data travels from the IoT device through the campus network to the backend server.

**Process:**
1. IoT device (VLAN 10/20/30/40) sends HTTP POST request.
2. Packet reaches the access switch on the device's VLAN.
3. Traffic trunked to the core/distribution switch.
4. Inter-VLAN routing forwards the packet to the server VLAN (VLAN 50).
5. ACLs permit HTTP/HTTPS traffic from IoT VLANs to the server.
6. Packet arrives at the backend server (192.168.50.10).

**Network Path Example (Computer Lab):**
```
IoT Meter (192.168.10.101, VLAN 10)
    → Access Switch (AccSW-Lab)
    → Trunk Link
    → Core L3 Switch (Inter-VLAN Routing)
    → Server VLAN 50
    → Backend Server (192.168.50.10)
```

> **Note:** In the initial prototype, the simulator and backend run on the same machine (localhost). The network layer is demonstrated separately via Cisco Packet Tracer.

---

### Step 3: Data Ingestion (Backend API)

**Component:** FastAPI Backend

The backend receives, validates, authenticates, and processes the incoming data.

**Process:**
1. FastAPI receives HTTP POST at `/api/energy/readings`.
2. **Authentication:** JWT token in the `Authorization` header is verified.
3. **Validation:** Pydantic model validates the JSON payload:
   - Required fields present
   - Data types correct
   - Values within expected ranges
4. **Processing:** Timestamp is normalized to UTC; calculated fields are verified.
5. **Response:** HTTP 201 (Created) returned with the stored reading ID.

**API Endpoint:**
```
POST /api/energy/readings
Headers:
  Authorization: Bearer <JWT_TOKEN>
  Content-Type: application/json
Body: <JSON payload from Step 1>
```

**Validation Rules:**
| Field | Validation |
|-------|-----------|
| `area_id` | Must match a registered campus area |
| `timestamp` | Valid ISO 8601 format, not in the future |
| `voltage` | 180.0 – 260.0 V |
| `current` | 0.0 – 100.0 A |
| `power` | 0.0 – 26000.0 W |
| `energy` | ≥ 0.0 kWh |
| `power_factor` | 0.0 – 1.0 |

---

### Step 4: Data Persistence (Database)

**Component:** SQLite Database

Validated energy readings are stored in the database for historical analysis.

**Process:**
1. The backend creates a new record in the `energy_readings` table.
2. A unique `reading_id` is auto-generated.
3. Server-side `received_at` timestamp is added.
4. The record is committed to the SQLite database.

**Database Record:**
| Column | Value |
|--------|-------|
| `reading_id` | 1 (auto-increment) |
| `area_id` | comp_lab_01 |
| `timestamp` | 2026-08-23T10:30:00Z |
| `voltage` | 228.5 |
| `current` | 12.3 |
| `power` | 2810.55 |
| `energy` | 45.67 |
| `power_factor` | 0.92 |
| `received_at` | 2026-08-23T10:30:01Z |

---

### Step 5: Data Analysis (AI/ML Engine)

**Component:** Scikit-learn ML Models

Historical data is analyzed to produce predictions and detect anomalies.

#### Step 5a: Energy Consumption Prediction

**Process:**
1. Query the last N hours/days of energy readings for an area.
2. Extract features: hour of day, day of week, rolling averages, etc.
3. Feed features into the trained regression model.
4. Model outputs predicted consumption for the next period.

**Input → Output:**
```
Input:  Historical readings for "Computer Laboratory" (last 7 days)
Output: Predicted consumption for next 24 hours = [45.2, 42.1, 38.7, ...] kWh
```

#### Step 5b: Anomaly Detection

**Process:**
1. Query recent energy readings for all areas.
2. Compare current reading against the learned baseline for that area/time.
3. Apply anomaly detection algorithm (e.g., Isolation Forest).
4. Flag readings that exceed the anomaly threshold.

**Input → Output:**
```
Input:  Current reading: 8500W at Computer Lab (normal: 2500-3500W)
Output: ANOMALY DETECTED
        - Area: Computer Laboratory
        - Severity: HIGH
        - Expected: 2500-3500W
        - Actual: 8500W
        - Possible Cause: Equipment malfunction or unauthorized usage
```

---

### Step 6: Results Storage

**Component:** SQLite Database

Prediction results and anomaly alerts are stored back in the database.

**Process:**
1. Prediction results are stored in the `predictions` table.
2. Anomaly alerts are stored in the `anomalies` table.
3. Each record is linked to the corresponding area and time period.

---

### Step 7: Visualization (Web Dashboard)

**Component:** React + Vite Frontend

The dashboard fetches and displays data through the REST API.

**Process:**
1. User logs in → receives JWT token.
2. Dashboard makes authenticated API requests:
   - `GET /api/dashboard/overview` → summary statistics
   - `GET /api/energy/readings?area=comp_lab_01&range=24h` → historical data
   - `GET /api/predictions/latest` → AI predictions
   - `GET /api/anomalies/active` → current anomaly alerts
3. React components render the data as:
   - Line charts (consumption over time)
   - Bar charts (area comparison)
   - Gauge charts (current consumption)
   - Alert cards (anomaly notifications)
   - Tables (detailed readings)

---

## 4. Data Flow Summary Table

| Step | Component | Input | Output | Protocol |
|------|-----------|-------|--------|----------|
| 1 | IoT Simulator | Time, area config | JSON reading | – |
| 2 | Campus Network | IP packet | Routed packet | TCP/IP |
| 3 | Backend API | JSON + JWT | Validated record | HTTP/REST |
| 4 | Database | Validated record | Stored row | SQL |
| 5a | ML Prediction | Historical data | Forecast values | Internal |
| 5b | ML Anomaly | Current + baseline | Anomaly alert | Internal |
| 6 | Database | ML results | Stored rows | SQL |
| 7 | Dashboard | API responses | Visual charts | HTTP/REST |

---

## 5. Communication Protocols

| Layer | Protocol | Port | Description |
|-------|----------|------|-------------|
| IoT → Backend | HTTP/HTTPS | 80/443 | RESTful API calls |
| Frontend → Backend | HTTP/HTTPS | 80/443 | RESTful API calls |
| Backend → Database | SQLite driver | – | File-based (local) |
| Network (future) | MQTT | 1883/8883 | Lightweight IoT messaging |

---

## 6. Data Format Standards

| Standard | Usage |
|----------|-------|
| **JSON** | All API request/response payloads |
| **ISO 8601** | All timestamps (e.g., `2026-08-23T10:30:00Z`) |
| **UTC** | All timestamps stored in UTC |
| **JWT** | Authentication tokens (header.payload.signature) |
| **HTTP Status Codes** | Standard REST response codes (200, 201, 400, 401, 404, 500) |

---

*Document Version: 1.0 | Created: August 2026*
