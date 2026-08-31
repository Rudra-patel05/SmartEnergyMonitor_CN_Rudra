# Smart Energy Monitor — Demonstration & Pre-Flight Checklist

> **GTU PBL Project — Quick Reference Pre-Flight Checklist**  
> **Use this checklist before starting any live presentation or evaluation.**

---

## 1. Pre-Flight Verification Checklist

- [ ] **Python Environment**: Python 3.10+ virtual environment activated.
- [ ] **Dependencies Installed**:
  - `pip install -r backend/requirements.txt`
  - `cd frontend && npm install`
- [ ] **Backend Server Active**:
  - Command: `python -m uvicorn app.main:app --port 8000` (run from `backend/` directory)
  - Verify at: `http://127.0.0.1:8000/docs`
- [ ] **Frontend Dashboard Active**:
  - Command: `npm run dev` (run from `frontend/` directory)
  - Verify at: `http://127.0.0.1:5173`
- [ ] **Database Seeded**:
  - `backend/energy.db` contains initial baseline readings.
- [ ] **ML Models Loaded**:
  - XGBoost model ready at `ai/models/xgboost_energy_model.json`.
  - Isolation Forest initialized in-memory on backend startup.

---

## 2. Default Access Credentials & Keys

| Resource | Identity / Key | Secret / Value | Purpose |
|---|---|---|---|
| **IoT Device Key** | `X-API-Key` | `iot_smart_energy_meter_key_2026_campus` | Telemetry HTTP Ingestion |
| **System Admin** | `admin` | `Admin@123!` | Full administrative access & JWT |
| **System Operator** | `operator` | `Operator@123!` | Operational access & telemetry query |
| **Auditor** | `auditor` | `Auditor@123!` | Read-only security audit inspection |

---

## 3. Key Demonstration Commands Quick-Reference

### A. Run Full System End-to-End Test
```bash
python backend/test_system_e2e.py
```
*(Expected Output: All 5 integration steps pass with 100% success)*

### B. Run Cybersecurity & Auth Suite
```bash
python backend/test_security.py
```
*(Expected Output: All 5 security tests pass with 100% success)*

### C. Stream Simulated IoT Telemetry
```bash
python iot/simulator.py --readings 5 --send-api
```
*(Streams 5 new simulated readings per device to the live backend)*

### D. Test Controlled Anomaly Detection
```bash
python backend/test_anomaly.py
```
*(Sends high-voltage / current spike payload and receives `status: ANOMALY`)*

### E. Build Production Frontend
```bash
cd frontend && npm run build
```
*(Verifies zero-error production bundle creation)*
