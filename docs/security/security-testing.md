# 🧪 Cybersecurity Verification & Security Testing Report

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Cybersecurity & Information Security (Day 12)  
> **Institution:** Gujarat Technological University – Computer Engineering

---

## 1. Test Objectives & Methodology

To verify that the Day 12 cybersecurity controls work as intended, we perform controlled security test cases covering user authentication, API access rules, device authorization, and data schema boundaries.

These tests are executed via `backend/test_security.py` directly hitting the FastAPI endpoints.

---

## 2. Security Test Matrix

| Test ID | Objective | Input Payload | Expected Status | Actual Status | Result |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **TEST-01** | Verify API rejects ingestion requests containing an invalid device API Key. | JSON telemetry payload + Header: `X-API-Key: wrong_key_12345` | **401 Unauthorized** | **401 Unauthorized** | **PASS** |
| **TEST-02** | Verify protected endpoints reject requests containing an invalid JWT token. | GET request + Header: `Authorization: Bearer invalid_jwt` | **401 Unauthorized** | **401 Unauthorized** | **PASS** |
| **TEST-03** | Verify API rejects ingestion requests containing a device ID with an invalid prefix. | JSON telemetry with `device_id: INVALID-01` | **422 Unprocessable**| **422 Unprocessable**| **PASS** |
| **TEST-04** | Verify API rejects telemetry values containing out-of-bounds parameters. | JSON telemetry with `temperature: 99.0` (limit: 60.0) | **422 Unprocessable**| **422 Unprocessable**| **PASS** |
| **TEST-05** | Verify successful user login, token issuance, and validation flow. | Username: `admin`, Password: `Admin@Campus2026!` | **200 OK** | **200 OK** | **PASS** |

---

## 3. Audit Log Output Logs (Mock / Typical Console Output)

```
[AUDIT LOG] 2026-08-31 12:35:00 - WARNING - Failed authentication attempt. Attempted Username: 'admin', IP: 127.0.0.1, Reason: Incorrect password or username
[AUDIT LOG] 2026-08-31 12:35:01 - INFO - Successful user login. Username: 'admin', Role: 'admin', IP: 127.0.0.1
[AUDIT LOG] 2026-08-31 12:35:02 - WARNING - Rejected malformed request payload at endpoint '/api/energy/readings'. Details: Validation failed (HTTP 422), IP: 127.0.0.1
```
---

## 4. Run Security Test Suite

To execute the automated security verification tests, run the following command from the project root:

```bash
python backend/test_security.py
```
This script runs in under 1 second, evaluating all 5 core security test conditions.
