# 🔑 Authentication & Authorization Framework

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Cybersecurity & Information Security (Day 12)  
> **Institution:** Gujarat Technological University – Computer Engineering

---

## 1. User Authentication Flow (FastAPI + JWT)

User access to prediction, anomaly status, and server administration is secured via **JSON Web Tokens (JWT)**.

```
Dashboard Client                      FastAPI Backend Auth Router
    │                                              │
    ├───── 1. POST Credentials (username/pass) ───>┤
    │                                              │ ──> [Verify hash via PBKDF2]
    │                                              │ <── [Generate JWT with role claim]
    ├<──── 2. HTTP 200: JSON Token Response ───────┤
    │                                              │
    │                                              │
Dashboard Client                      API Endpoints (Prediction/Anomaly)
    │                                              │
    ├───── 3. GET /predict (Bearer JWT) ──────────>┤
    │                                              │ ──> [Decrypt & Validate HS256]
    │                                              │ <── [Process ML Inference]
    ├<──── 4. HTTP 200: JSON Payload Response ─────┤
    │                                              │
```

### 1.1. Password Hashing Specification
Plaintext user passwords are never stored in the database. When a user is registered, their password is processed using:
- **Algorithm:** PBKDF2-HMAC-SHA256
- **Salt Size:** 16 bytes (securely generated via `secrets.token_hex`)
- **Iteration Count:** 100,000 rounds
- **Storage Format:** `<salt>$<derived_key_hex>`

To prevent timing-attack vulnerability, hash verification uses Python's `hmac.compare_digest` to perform a constant-time comparison.

---

## 2. Device Authentication (API Key Mechanism)

Because microcontrollers simulating IoT energy meters have constrained computing power, generating and verifying RSA signatures or maintaining active OIDC sessions on the edge is impractical. 

The system implements a **Pre-shared API Key** authentication mechanism:
- **Header Field:** `X-API-Key`
- **Verification Method:** Constant-time validation check on backend API router endpoints.
- **Access Level:** Grants permission to write readings (`POST /api/energy/readings` and `/bulk`).

---

## 3. Demo Roles & Credentials

For academic demonstration, the following local demo accounts are pre-configured in `backend/app/auth.py`:

| Username | Role | Full Name | Default Password | Access Level |
| :--- | :--- | :--- | :--- | :--- |
| **admin** | `admin` | Campus Network & Energy Administrator | `Admin@Campus2026!` | Read & Write All, System configuration status, API logs |
| **operator** | `operator` | Facility Energy Operations Staff | `Operator@123!` | Read readings, trigger ML predictions, check anomalies |
| **IoT Device** | `iot_device` | Simulated Energy Meter Node | `X-API-Key: iot_smart_energy_meter_key_2026_campus` | Write energy telemetry readings |
