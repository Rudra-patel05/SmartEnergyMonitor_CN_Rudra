# 🛡️ Cybersecurity Architecture

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Cybersecurity & Information Security (Day 12)  
> **Institution:** Gujarat Technological University – Computer Engineering

---

## 1. Security Design Principles

The security architecture of the Smart Campus Energy Monitor is designed around the concept of **Defense in Depth** and **Zero Trust**. The system is partitioned into independent layers to ensure that if one layer is compromised, the remaining layers continue to protect sensitive campus resources.

```
                  ┌────────────────────────────────────────┐
                  │          Cisco Network ACLs            │
                  │   (VLAN Segmentation & Micro-sec)      │
                  └──────────────────┬─────────────────────┘
                                     │
                  ┌──────────────────┴─────────────────────┐
                  │        REST API Key Authentication     │
                  │      (Simulator Ingestion Security)    │
                  └──────────────────┬─────────────────────┘
                                     │
                  ┌──────────────────┴─────────────────────┐
                  │       JSON Web Token (JWT) Security    │
                  │     (Dashboard Session Management)     │
                  └──────────────────┬─────────────────────┘
                                     │
                  ┌──────────────────┴─────────────────────┐
                  │        Strict Input Schema Bounds      │
                  │    (Pydantic Range & Regex Filtering)  │
                  └────────────────────────────────────────┘
```

---

## 2. Threat Modeling & Mitigation Matrix

| Threat Vector | Description | Targeted System Component | Architectural Mitigation |
| :--- | :--- | :--- | :--- |
| **Spoofed Telemetry Injection** | Rogue node injecting fake high/low energy readings to manipulate ML predictions. | Ingestion API (`POST /readings`) | Device authentication using pre-shared **`X-API-Key`** headers and strict **Pydantic schema bounds** verification. |
| **Eavesdropping & Packet Sniffing** | Capturing plaintext credentials or sensor telemetry on the local network. | Local Link Layer (Ethernet/VLAN) | Enforce IEEE **802.1Q VLAN isolation** and mandate **HTTPS/TLS** in production specifications. |
| **Lateral Privilege Escalation** | Compromised IoT MCU scanning the network to attack administrative or server subnets. | Switch Access Ports | Enforce **Cisco Extended ACLs** restricting IoT VLANs to communicating exclusively with port 8000 of the Server. |
| **Brute Force & Credential Stuffing** | Attackers attempts to guess administrative dashboard passwords. | Login Endpoint (`POST /auth/token`) | **PBKDF2-HMAC-SHA256** password hashing with cryptographically secure random salts and constant-time comparison. |
| **JWT Alteration & Session Hijacking** | Forging administrative tokens or extending token expiration window. | API Routers (`/api/prediction`, `/api/anomaly`) | HS256 signature verification using a high-entropy secret key (`SECRET_KEY`) with automatic token expiration. |

---

## 3. Production Hardening Recommendations

While this prototype implementation uses local configuration options for demonstration:
1. **Transport Layer Security (TLS/HTTPS):** Run FastAPI behind a reverse proxy (e.g. Nginx or Traefik) configured with Let's Encrypt SSL/TLS certificates to encrypt all data-in-transit.
2. **Database Hardening:** Migrate from local file-based SQLite to a production-grade PostgreSQL database running in a private server subnet with password authentication.
3. **Environment Secrets Management:** Store keys (`SECRET_KEY`, `SMART_ENERGY_API_KEY`) in a secure secrets manager (e.g., HashiCorp Vault or environment variables) instead of plaintext configuration files.
