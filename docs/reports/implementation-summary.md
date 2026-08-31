# Smart Energy Monitor & Network Architecture — Implementation Summary

> **GTU PBL Project — Days 1 to 13 Final Implementation Overview**  
> **Repository**: `SmartEnergyMonitor_CN`  
> **Status**: Complete & Verified (All 13 Milestones Delivered)

---

## 1. Executive Summary

**SmartEnergyMonitor_CN** is an end-to-end, enterprise-grade Smart Campus Energy Monitoring and Network Infrastructure solution. The system captures simulated IoT telemetry across five campus zones, transmits data securely over a segmented computer network, persists readings in SQLite, exposes high-performance REST APIs via FastAPI, serves an interactive React dashboard, provides AI-driven energy predictions (XGBoost) and unsupervised anomaly detection (Isolation Forest), and implements multi-layer cybersecurity controls (JWT, API Keys, Structured Audit Logging, and Cisco IOS ACLs).

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

## 2. Completed Milestones Breakdown (Days 1–13)

| Day | Milestone | Key Deliverables & Achievements |
|---|---|---|
| **Day 1** | **Project Foundation** | Project directory structure, virtual environment setup, package manifests (`requirements.txt`, `package.json`), Git repo initialization. |
| **Day 2** | **Virtual IoT Simulator** | Multi-zone synthetic energy meter simulator (`iot/simulator.py`, `iot/devices.py`) modeling 5 devices (LAB-01, LAB-02, CLASS-01, LIB-01, ADMIN-01) with noise and occupancy physics. |
| **Day 3** | **FastAPI + SQLite** | Asynchronous REST backend (`backend/app/main.py`), SQLAlchemy ORM schema (`models.py`), Pydantic validation (`schemas.py`), SQLite storage (`energy.db`). |
| **Day 4** | **IoT-to-FastAPI HTTP Pipeline** | Automated HTTP client (`iot/api_client.py`) streaming telemetry directly into `/api/energy/readings` with batching, retry logic, and error resilience. |
| **Day 5** | **ML Data Preparation** | Raw dataset cleaning, feature engineering (`hour`, `day_of_week`, `is_weekend`, `power_rolling_mean_3`, `energy_delta`), train/test splitting (`ai/src/data_preparation.py`). |
| **Day 6** | **XGBoost Energy Prediction** | Supervised gradient boosting regression pipeline (`ai/src/train_xgboost.py`), hyperparameter tuning, model artifact export (`xgboost_energy_model.json`), RMSE/MAE evaluation. |
| **Day 7** | **Isolation Forest Anomaly Engine** | Unsupervised anomaly detection model (`ai/src/anomaly_detection.py`), synthetic fault injection evaluation benchmark, precision/recall/F1 scoring, score visualization. |
| **Day 8** | **React Dashboard Foundation** | Premium dark-mode dashboard (`frontend/`), KPI cards, live telemetry feeds, Recharts interactive time-series plots, responsive grid layout. |
| **Day 9** | **XGBoost Integration** | Real-time predictive analytics router (`backend/app/routes/prediction.py`), frontend prediction forecast card, next 15-min energy consumption preview. |
| **Day 10** | **Anomaly Detection Integration** | Real-time anomaly scoring router (`backend/app/routes/anomaly.py`), in-memory Isolation Forest service, dashboard anomaly badge, manual anomaly inspection tool. |
| **Day 11** | **Computer Network Architecture** | Enterprise VLAN 10-50 design, IPv4 subnetting (`/24`, `/27`), Router-on-a-Stick (ROAS) sub-interfaces (`Gig0/0.10-50`), Cisco IOS ACLs, Packet Tracer deployment guide. |
| **Day 12** | **Cybersecurity & Hardening** | JWT auth (`HS256`, `PBKDF2-HMAC-SHA256`), Device API key headers (`X-API-Key`), structured audit logger middleware, strict Pydantic bounds, automated security test suite. |
| **Day 13** | **Full System Integration & Verification** | End-to-end integration test (`backend/test_system_e2e.py`), multi-scenario verification, regression test pass, comprehensive final documentation. |

---

## 3. Architecture Specification

### 3.1 Network Architecture (Day 11)
- **VLAN Segmentation**:
  - `VLAN 10` — IoT Sensors (`192.168.10.0/24`, Gateway: `192.168.10.1`)
  - `VLAN 20` — Application & Database Servers (`192.168.20.0/24`, Gateway: `192.168.20.1`)
  - `VLAN 30` — User Workstations & Dashboard Clients (`192.168.30.0/24`, Gateway: `192.168.30.1`)
  - `VLAN 40` — Network Management (`192.168.40.0/27`, Gateway: `192.168.40.1`)
  - `VLAN 50` — DMZ & External Services (`192.168.50.0/27`, Gateway: `192.168.50.1`)
- **Inter-VLAN Routing**: Cisco 2911 Router running Router-on-a-Stick (ROAS) with `802.1Q` encapsulation on sub-interfaces `Gig0/0.10` through `Gig0/0.50`.
- **Cisco IOS ACL Policy**: Strict micro-segmentation where IoT devices can only push HTTP (`TCP 8000`) to the Backend Server (`192.168.20.10`) and are blocked from directly pinging or reaching user workstations or management consoles.

### 3.2 Backend & Data Storage (Days 3, 4, 12)
- **Framework**: FastAPI with Uvicorn ASGI server.
- **Database**: SQLite (`energy.db`) via SQLAlchemy ORM with connection pooling.
- **Telemetry Ingestion**: Authenticated endpoint `POST /api/energy/readings` with Pydantic v2 validation.
- **Audit Logging**: Asynchronous logging middleware tracking every HTTP request, response time, validation failure, and unauthorized attempt with client IP in `logs/audit.log`.

### 3.3 Machine Learning Pipeline (Days 5, 6, 7, 9, 10)
- **XGBoost Regressor**:
  - Objective: Forecast next 15-minute interval energy consumption ($E_{t+1}$).
  - Features: `power`, `current`, `voltage`, `temperature`, `occupancy`, `hour`, `day_of_week`, `is_weekend`, `power_rolling_mean_3`, `energy_delta`.
  - Artifact: `ai/models/xgboost_energy_model.json`.
- **Isolation Forest Classifier**:
  - Objective: Unsupervised multi-variable anomaly detection ($score < 0 \implies \text{Anomaly}$).
  - Features: 8 rolling and instantaneous telemetry features.
  - Hyperparameters: `n_estimators=150`, `contamination=0.04`, `random_state=42`.

### 3.4 Cybersecurity Hardening (Day 12)
- **User Authentication**: OAuth2 Password Flow emitting signed HS256 JWT tokens. Passwords hashed using PBKDF2-HMAC-SHA256 with cryptographically secure random 16-byte salts.
- **Device Authentication**: Hardware IoT meters authenticate using pre-shared secret key headers (`X-API-Key: iot_smart_energy_meter_key_2026_campus`).
- **Input Validation**: Strict bounds on all numeric fields (e.g., Voltage: 180V-280V, Current: 0-100A, Temperature: -20°C-60°C, Power: 0-30000W) and regex-enforced Device ID patterns (`^(LAB|CLASS|LIB|ADMIN)-[0-9A-Za-z_-]+$`).

---

## 4. Final System Verification Status

All components have been verified via automated test suites and end-to-end integration scripts:
- **E2E Integration Test**: `100% Passed` (`backend/test_system_e2e.py`)
- **Cybersecurity Suite**: `100% Passed` (`backend/test_security.py`)
- **API Unit Suite**: `100% Passed` (`backend/test_api.py`)
- **Anomaly Detection Test**: `100% Passed` (`backend/test_anomaly.py`)
- **IoT Live Push Simulation**: `5/5 Readings Accepted` (`iot/simulator.py --send-api`)
- **Frontend Dashboard Build**: `0 Errors` (`npm run build`)
