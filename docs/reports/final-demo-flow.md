# Smart Energy Monitor & Network Architecture — Final Demonstration Flow

> **GTU PBL Demonstration & Live Presentation Guide**  
> **Target Audience**: Evaluators, Faculty, Project Examiners  
> **Duration**: 10–15 Minutes

---

## 1. Demonstration Environment Setup

Before starting the live demonstration, ensure the following services are active:

| Service | Port / URL | Start Command |
|---|---|---|
| **FastAPI Backend** | `http://127.0.0.1:8000` | `cd backend && python -m uvicorn app.main:app --port 8000` |
| **Interactive API Docs** | `http://127.0.0.1:8000/docs` | Built-in Swagger UI |
| **React Dashboard** | `http://127.0.0.1:5173` | `cd frontend && npm run dev` |

---

## 2. Six Demonstration Scenarios Walkthrough

### Scenario 1: Live IoT Telemetry Ingestion & Real-Time Dashboard Updates
* **Goal**: Demonstrate simulated IoT meters transmitting real-time sensor metrics to the backend.
* **Action**:
  1. Open the React Dashboard at `http://127.0.0.1:5173`.
  2. Open a terminal and run the virtual IoT simulator:
     ```bash
     python iot/simulator.py --readings 2 --send-api
     ```
  3. Observe terminal confirmation: `Sent: 5, Successful: 5, Failed: 0`.
  4. Switch to the React Dashboard and point out:
     - The **Total Readings** and **System Average Power** KPI cards automatically refresh.
     - Device telemetry charts update with the latest readings.

---

### Scenario 2: XGBoost Machine Learning Predictive Analytics
* **Goal**: Demonstrate AI-driven energy consumption forecasting for the next 15-minute window.
* **Action**:
  1. In the React Dashboard, navigate to the **XGBoost Prediction** section.
  2. Select device `LAB-01` from the dropdown selector.
  3. Click **"Predict Next Energy Consumption"**.
  4. Show the prediction output card displaying:
     - Predicted Next Energy (kWh)
     - Current Baseline Energy
     - Confidence Indicator and Model Used (`XGBoost`)
  5. Explain the underlying ML architecture: 10 input features including rolling power averages, time-of-day temporal encoding, and occupancy correlation.

---

### Scenario 3: Unsupervised Isolation Forest Anomaly Detection
* **Goal**: Demonstrate immediate identification of physical anomalies (surges, off-hours spikes).
* **Action**:
  1. On the dashboard, view the **Anomaly Status** badge for all campus meters.
  2. Demonstrate controlled anomaly injection using the interactive tool or terminal:
     ```bash
     python backend/test_anomaly.py
     ```
  3. Show the JSON response received from `POST /api/anomaly/check`:
     ```json
     {
       "device_id": "LAB-TEST",
       "anomaly_flag": 1,
       "anomaly_score": -0.08498,
       "status": "ANOMALY"
     }
     ```
  4. Explain to the evaluator that the Isolation Forest operates without labels and isolates anomalies with short path lengths in isolation trees.

---

### Scenario 4: Cybersecurity Protection (Authentication & Access Control)
* **Goal**: Demonstrate rejection of unauthorized clients and API tampering.
* **Action**:
  1. In terminal or Swagger docs (`/docs`), submit a telemetry payload with a forged API Key:
     ```bash
     curl -X POST http://127.0.0.1:8000/api/energy/readings \
       -H "Content-Type: application/json" \
       -H "X-API-Key: invalid_hacker_key" \
       -d '{"device_id":"LAB-01","area":"Computer Laboratory 1","timestamp":"2026-08-31 12:00:00","voltage":230,"current":1,"power":230,"energy":1,"temperature":25,"occupancy":10}'
     ```
  2. Show the immediate HTTP `401 Unauthorized` rejection:
     `{"detail": "Invalid device API Key."}`
  3. Demonstrate JWT user authentication: Login as `admin` (`Admin@123!`) at `POST /api/auth/token` to receive a signed JWT token.

---

### Scenario 5: Input Boundary Validation & Structured Audit Logging
* **Goal**: Demonstrate defense against malformed data, buffer exploits, and audit traceability.
* **Action**:
  1. Attempt to post an out-of-bounds reading (e.g., `temperature = 99.0°C`):
     ```bash
     curl -X POST http://127.0.0.1:8000/api/energy/readings \
       -H "Content-Type: application/json" \
       -H "X-API-Key: iot_smart_energy_meter_key_2026_campus" \
       -d '{"device_id":"LAB-01","area":"Computer Laboratory 1","timestamp":"2026-08-31 12:00:00","voltage":230,"current":1,"power":230,"energy":1,"temperature":99.0,"occupancy":10}'
     ```
  2. Show HTTP `422 Unprocessable Entity` rejection.
  3. Show the generated structured audit log in `backend/app/main.py` console output:
     `[AUDIT LOG] Rejected malformed request payload at endpoint '/api/energy/readings'. Details: Validation failed (HTTP 422)`

---

### Scenario 6: Computer Network Architecture & Micro-Segmentation
* **Goal**: Present the Cisco network infrastructure, VLAN segregation, and ACL security policies.
* **Action**:
  1. Open `network/topology/topology_specification.md` and `network/README.md`.
  2. Show the **Topology Diagram**:
     - `VLAN 10` (IoT Sensors: `192.168.10.0/24`)
     - `VLAN 20` (Servers: `192.168.20.0/24`)
     - `VLAN 30` (Workstations: `192.168.30.0/24`)
     - `VLAN 40` (Management: `192.168.40.0/27`)
  3. Present the **Router-on-a-Stick (ROAS)** sub-interface configuration (`Gig0/0.10` - `Gig0/0.50`).
  4. Explain the **Cisco Extended ACL (ACL 110)**:
     - Permits IoT meters on VLAN 10 to send HTTP (`TCP 8000`) exclusively to the backend server (`192.168.20.10`).
     - Denies IoT meters from initiating connections to user workstations (VLAN 30) or management subnets (VLAN 40).

---

## 3. Evaluator Q&A Preparation

| Potential Examiner Question | Recommended Key Response |
|---|---|
| *Why use synthetic data rather than physical sensors?* | "Physical energy monitoring requires high-voltage electrical grid tapping. The virtual simulator accurately models voltage fluctuations, power factor variations, thermal dynamics, and occupancy correlation across 5 distinct campus buildings." |
| *Why use Isolation Forest for anomaly detection?* | "Energy faults and surges are rare and unlabelled in real campus networks. Isolation Forest isolates anomalies efficiently ($O(n \log n)$) without requiring pre-labeled training classes." |
| *How does the network protect the server if an IoT sensor is compromised?* | "Hardware micro-segmentation in VLAN 10 and Cisco Extended ACLs restrict the sensor to only transmitting TCP 8000 to 192.168.20.10. Lateral movement to workstations or management interfaces is blocked at the router boundary." |
