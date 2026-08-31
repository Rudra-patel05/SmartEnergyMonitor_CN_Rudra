# 🏫 AI-Driven Smart Energy Consumption Monitoring and Prediction System for Smart Campus

> **Gujarat Technological University – Computer Engineering**  
> **Subject:** Computer Networks – PBL (Complex Problem Solving Project)  
> **Repository:** `SmartEnergyMonitor_CN`  
> **Status:** 100% Completed & Verified (Days 1 to 13)

---

## 📋 Project Overview

**SmartEnergyMonitor_CN** is an end-to-end smart campus energy intelligence, predictive forecasting, and secure network infrastructure platform. The system models multi-zone IoT sensor telemetry, routes data across an enterprise segmented campus network, persists time-series readings in SQLite, exposes high-speed REST APIs via FastAPI, renders a real-time React dashboard, predicts future energy consumption using XGBoost, detects consumption anomalies using Isolation Forest, and enforces multi-layer cybersecurity (JWT, API keys, structured audit logging, input validation bounds, and Cisco IOS ACLs).

```
+----------------------------------------------------------------------------------------------------+
|                                    CAMPUS NETWORK ARCHITECTURE                                     |
|                                                                                                    |
|  [VLAN 10: IoT Sensors]       [VLAN 20: Servers]       [VLAN 30: Workstations]   [VLAN 40: Mgmt]   |
|   192.168.10.0/24              192.168.20.0/24          192.168.30.0/24           192.168.40.0/24  |
|   (Virtual Meters)             (FastAPI + ML + DB)      (React Dashboard)         (SysAdmin SSH)   |
|         │                             │                        │                         │         |
|         └───────────────┬─────────────┴────────────────────────┴─────────────────────────┘         |
|                         │ 802.1Q Trunks                                                            |
|                   [Cisco 2960 Core Switch] ─── Gig0/1 ─── [Cisco 2911 ROAS Router]                 |
|                   (Hardware Micro-Segmentation & Extended Access Control Lists)                   |
+----------------------------------------------------------------------------------------------------+
                                                │
                                                ▼
+----------------------------------------------------------------------------------------------------+
|                                      FULL-STACK SOFTWARE STACK                                     |
|                                                                                                    |
|  +─────────────────────────+      HTTP/JSON + API Key       +───────────────────────────────────+  |
|  |   Virtual IoT Meter     | ─────────────────────────────► |        FastAPI Backend API        |  |
|  |  (5 Campus Zones Sim)   |                                |  (Auth, Telemetry, ML Routers)    |  |
|  +─────────────────────────+                                +───────────────────────────────────+  |
|                                                                    │              │                |
|                                                     SQLAlchemy ORM │              │ Scikit-Learn   |
|                                                                    ▼              ▼ / XGBoost      |
|  +─────────────────────────+      Bearer JWT Auth           +──────────────+ +──────────────────+  |
|  |     React Dashboard     | ◄───────────────────────────── |  SQLite DB   | | Machine Learning |  |
|  |  (Live Charts, Alerts)  |                                | (Persistent) | | (IForest + XGB)  |  |
|  +─────────────────────────+                                +──────────────+ +──────────────────+  |
+----------------------------------------------------------------------------------------------------+
```

---

## 🛠️ Technology Stack

| Layer | Technologies / Frameworks |
|---|---|
| **Frontend** | React 19, Vite, Recharts, Lucide Icons, Vanilla CSS Design System |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, SQLAlchemy ORM, Pydantic v2 |
| **Database** | SQLite (`energy.db`) with foreign key constraints & connection pooling |
| **Machine Learning** | XGBoost (Energy Forecasting), Scikit-Learn (Isolation Forest Anomaly Detection), Pandas, NumPy |
| **Network Infrastructure** | Cisco IOS CLI, Router-on-a-Stick (ROAS), 802.1Q Trunking, Extended ACLs (Cisco Packet Tracer 8.x) |
| **Cybersecurity** | JWT (HS256, PBKDF2-HMAC-SHA256), Device API Keys (`X-API-Key`), Middleware Audit Logging, Strict Bounds |

---

## 📅 Project Development Roadmap (Days 1–13)

| Day | Milestone | Summary of Achievements | Status |
|---|---|---|---|
| **Day 1** | **Project Foundation** | Architecture design, repository initialization, environment setup. | ✅ Completed |
| **Day 2** | **Virtual IoT Simulator** | 5-zone realistic energy meter generator with noise and occupancy models. | ✅ Completed |
| **Day 3** | **FastAPI + SQLite** | REST backend, database schema, Pydantic schemas, Swagger UI. | ✅ Completed |
| **Day 4** | **IoT-to-API HTTP Pipeline** | Automated HTTP telemetry client with batching and error recovery. | ✅ Completed |
| **Day 5** | **ML Data Preparation** | Dataset cleaning, rolling feature engineering, temporal transformations. | ✅ Completed |
| **Day 6** | **XGBoost Energy Prediction** | Supervised gradient boosting regression pipeline and model export. | ✅ Completed |
| **Day 7** | **Isolation Forest Anomaly Engine** | Unsupervised anomaly model and synthetic fault evaluation benchmark. | ✅ Completed |
| **Day 8** | **React Dashboard Foundation** | Dark-mode telemetry dashboard with live metric cards and charts. | ✅ Completed |
| **Day 9** | **XGBoost Integration** | Real-time predictive analytics router and frontend forecasting card. | ✅ Completed |
| **Day 10** | **Anomaly Detection Integration** | Anomaly checking endpoint, in-memory service, and dashboard alerts. | ✅ Completed |
| **Day 11** | **Computer Network Architecture** | Enterprise VLAN 10-50 scheme, ROAS routing, and Cisco IOS ACLs. | ✅ Completed |
| **Day 12** | **Cybersecurity & Hardening** | JWT auth, device API key validation, structured audit logger, Pydantic bounds. | ✅ Completed |
| **Day 13** | **Final System Integration & Verification** | End-to-end testing, multi-scenario demonstration, comprehensive reports. | ✅ Completed |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (with `pip`)
- Node.js 18+ (with `npm`)

### 2. Backend Setup
```bash
# Navigate to backend and install requirements
cd backend
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn app.main:app --port 8000
```
* Interactive API Documentation (Swagger UI): `http://127.0.0.1:8000/docs`
* Alternative Documentation (ReDoc): `http://127.0.0.1:8000/redoc`

### 3. Frontend Dashboard Setup
```bash
# Navigate to frontend and start dev server
cd frontend
npm install
npm run dev
```
* Dashboard URL: `http://127.0.0.1:5173`

### 4. Running the Virtual IoT Simulator
```bash
# Generate and stream live simulated telemetry to the backend API
python iot/simulator.py --readings 5 --send-api
```

### 5. Automated Verification & Testing
```bash
# Run End-to-End System Integration Test
python backend/test_system_e2e.py

# Run Cybersecurity & Access Control Test Suite
python backend/test_security.py

# Run Dedicated Anomaly Detection Test
python backend/test_anomaly.py

# Run Backend Unit Test
python backend/test_api.py
```

---

## 🔐 Security & Access Credentials

| Identity / Key | Value | Role / Permissions |
|---|---|---|
| `X-API-Key` Header | `iot_smart_energy_meter_key_2026_campus` | IoT Telemetry Ingestion (`POST /api/energy/readings`) |
| User: `admin` | `Admin@123!` | System Administrator (Full Access, JWT Auth) |
| User: `operator` | `Operator@123!` | Energy Operator (Telemetry Query, Predictions) |
| User: `auditor` | `Auditor@123!` | Security Auditor (Read-only Log Inspection) |

---

## 🌐 Network Architecture Highlights

- **VLAN 10** (`192.168.10.0/24`): IoT Smart Meters (Gateway: `192.168.10.1`)
- **VLAN 20** (`192.168.20.0/24`): Servers & Database (Gateway: `192.168.20.1`, Backend: `192.168.20.10`)
- **VLAN 30** (`192.168.30.0/24`): User Workstations (Gateway: `192.168.30.1`)
- **VLAN 40** (`192.168.40.0/27`): Network Management (Gateway: `192.168.40.1`)
- **VLAN 50** (`192.168.50.0/27`): DMZ & Public Gateways (Gateway: `192.168.50.1`)
- **Access Control (ACL 110)**: Strict micro-segmentation allowing IoT meters to push HTTP data only to the backend server while denying inter-VLAN access to workstations or management interfaces.

---

## 📂 Project Directory Structure

```
SmartEnergyMonitor_CN/
├── ai/                               # Machine Learning Module
│   ├── data/                         # Datasets (raw, processed, anomaly)
│   ├── models/                       # Exported ML model artifacts (XGBoost JSON)
│   └── src/                          # Training, preprocessing & evaluation scripts
├── backend/                          # FastAPI Backend Application
│   ├── app/
│   │   ├── routes/                   # API routers (auth, energy, prediction, anomaly)
│   │   ├── services/                 # ML inference services (anomaly_service.py)
│   │   ├── auth.py                   # JWT & API key security logic
│   │   ├── database.py               # SQLAlchemy database engine
│   │   ├── logger.py                 # Structured security audit logger
│   │   ├── main.py                   # FastAPI entrypoint & middleware
│   │   ├── models.py                 # SQLite ORM models
│   │   └── schemas.py                # Pydantic validation schemas
│   ├── energy.db                     # SQLite persistent storage
│   ├── test_security.py              # Cybersecurity test suite
│   ├── test_system_e2e.py            # End-to-end integration test
│   └── requirements.txt              # Python dependencies
├── docs/                             # Project Documentation
│   ├── architecture/                 # System and data flow diagrams
│   ├── reports/                      # Implementation summary, testing, demo flows
│   └── security/                     # Cybersecurity architecture & specs
├── frontend/                         # React 19 + Vite Dashboard
│   ├── src/                          # UI components, charts, and API client
│   └── package.json                  # Frontend dependencies
├── iot/                              # Virtual IoT Sensor Simulator
│   ├── api_client.py                 # Authenticated HTTP client
│   ├── config.py                     # Simulator configuration
│   ├── devices.py                    # Energy meter simulation models
│   └── simulator.py                  # Simulator CLI executable
├── network/                          # Computer Network Architecture
│   ├── documentation/                # IP addressing, VLAN design, routing, ACLs
│   └── topology/                     # Cisco IOS CLI scripts & Packet Tracer guide
└── README.md                         # Project overview
```

---

## 📜 Academic Attribution & License

Developed as part of the Gujarat Technological University (GTU) Computer Engineering curriculum for **Computer Networks – Complex Problem Solving (PBL)**.