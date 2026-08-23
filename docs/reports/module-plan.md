# Module Plan

> AI-Driven Smart Energy Consumption Monitoring and Prediction System for Smart Campus

---

## Overview

The project is decomposed into **ten modules**, each responsible for a specific aspect of the system. This document defines each module's purpose, scope, key components, dependencies, and planned implementation phase.

---

## Module 1: IoT Simulator

### Purpose
Generate realistic simulated energy consumption data for four campus areas without requiring physical hardware.

### Scope
- Simulate energy meters for: Computer Laboratory, Classroom, Library, Administrative Office
- Generate readings with configurable intervals
- Produce realistic patterns based on time, area type, and day of week

### Key Components
| Component | Description |
|-----------|-------------|
| `iot/simulator.py` | Main simulator engine |
| `iot/config.py` | Area configurations and parameters |
| `iot/data_sender.py` | HTTP client to send readings to backend API |
| `iot/profiles/` | Energy consumption profiles per area type |

### Data Fields Generated
- `area_id`, `area_name`, `timestamp`
- `voltage` (V), `current` (A), `power` (W), `energy` (kWh), `power_factor`

### Dependencies
- Python 3.11+
- `requests` library (for API communication)
- Backend API must be running to receive data

### Implementation Phase
Phase 2

---

## Module 2: Network Communication

### Purpose
Design and simulate the campus network infrastructure demonstrating Computer Networks concepts.

### Scope
- Campus network topology design
- VLAN segmentation for IoT, server, and management traffic
- Inter-VLAN routing configuration
- Access Control Lists (ACLs) for security
- IP addressing scheme

### Key Components
| Component | Description |
|-----------|-------------|
| `network/campus_network.pkt` | Cisco Packet Tracer simulation file |
| `network/configs/` | Switch and router configuration scripts |
| `docs/architecture/network-architecture.md` | Network design documentation |

### Network Concepts Demonstrated
- VLAN configuration and trunking
- Inter-VLAN routing (SVI / Router-on-a-stick)
- IPv4 subnetting and addressing
- ACL-based traffic filtering
- Port security

### Dependencies
- Cisco Packet Tracer 8.0+

### Implementation Phase
Phase 6

---

## Module 3: Backend API

### Purpose
Serve as the central data processing hub — receiving IoT data, serving the dashboard, and integrating AI models.

### Scope
- RESTful API design and implementation
- Data ingestion from IoT simulator
- Data retrieval for dashboard
- AI model integration for predictions and anomalies
- Request validation and error handling

### Key Components
| Component | Description |
|-----------|-------------|
| `backend/main.py` | FastAPI application entry point |
| `backend/routers/` | API route handlers (energy, auth, predictions, anomalies) |
| `backend/models/` | SQLAlchemy ORM models |
| `backend/schemas/` | Pydantic request/response schemas |
| `backend/services/` | Business logic layer |
| `backend/core/` | Configuration, security, and database setup |

### API Endpoint Groups
| Group | Base Path |
|-------|-----------|
| Authentication | `/api/auth/` |
| Energy Data | `/api/energy/` |
| Campus Areas | `/api/areas/` |
| Predictions | `/api/predictions/` |
| Anomalies | `/api/anomalies/` |
| Dashboard | `/api/dashboard/` |

### Dependencies
- Python 3.11+, FastAPI, Uvicorn, SQLAlchemy, Pydantic

### Implementation Phase
Phase 2–3

---

## Module 4: Database

### Purpose
Persist all energy data, user accounts, AI results, and system configuration.

### Scope
- Database schema design
- Table creation and migration
- Data access layer (CRUD operations)
- Query optimization with indexes

### Key Components
| Component | Description |
|-----------|-------------|
| `backend/core/database.py` | Database connection and session management |
| `backend/models/` | SQLAlchemy model definitions |
| `backend/core/init_db.py` | Database initialization and seeding |

### Tables (Planned)
| Table | Purpose |
|-------|---------|
| `users` | User accounts, hashed passwords, roles |
| `campus_areas` | Area definitions and metadata |
| `energy_readings` | Raw energy consumption data |
| `predictions` | ML prediction outputs |
| `anomalies` | Detected anomaly records |

### Technology
- **Initial:** SQLite (zero-configuration, file-based)
- **Future:** PostgreSQL (production/cloud deployment)

### Dependencies
- SQLAlchemy, SQLite3 (built into Python)

### Implementation Phase
Phase 2

---

## Module 5: AI Prediction

### Purpose
Train and deploy a machine learning model to predict future energy consumption based on historical data.

### Scope
- Feature engineering from raw energy data
- Model training and evaluation
- Model persistence (save/load)
- Prediction API integration

### Key Components
| Component | Description |
|-----------|-------------|
| `ai/prediction/model.py` | Prediction model training and inference |
| `ai/prediction/features.py` | Feature engineering pipeline |
| `ai/prediction/evaluate.py` | Model evaluation and metrics |
| `ai/models/` | Saved model files (.joblib) |

### Approach
| Aspect | Detail |
|--------|--------|
| **Type** | Supervised regression |
| **Algorithms** | Linear Regression, Random Forest, Gradient Boosting |
| **Features** | Hour, day of week, area type, rolling averages, lag features |
| **Target** | Energy consumption (kWh) for next period |
| **Metrics** | MAE, RMSE, R² score |

### Dependencies
- scikit-learn, pandas, numpy, joblib

### Implementation Phase
Phase 4

---

## Module 6: Anomaly Detection

### Purpose
Detect unusual energy consumption patterns that may indicate equipment malfunction, unauthorized usage, or data errors.

### Scope
- Baseline computation per area and time slot
- Anomaly scoring and classification
- Severity assignment (low, medium, high)
- Alert generation

### Key Components
| Component | Description |
|-----------|-------------|
| `ai/anomaly/detector.py` | Anomaly detection model |
| `ai/anomaly/baseline.py` | Historical baseline computation |
| `ai/anomaly/alerts.py` | Alert generation and severity classification |

### Approach
| Aspect | Detail |
|--------|--------|
| **Type** | Unsupervised / semi-supervised |
| **Algorithms** | Isolation Forest, Z-Score, One-Class SVM |
| **Input** | Current reading vs. historical baseline |
| **Output** | Anomaly flag, severity, description |

### Dependencies
- scikit-learn, pandas, numpy

### Implementation Phase
Phase 4

---

## Module 7: Dashboard

### Purpose
Provide an interactive web interface for campus administrators to monitor energy data, view AI insights, and manage the system.

### Scope
- User login/logout
- Real-time energy consumption display
- Historical trend charts
- AI prediction visualization
- Anomaly alert panel
- Area comparison views

### Key Components
| Component | Description |
|-----------|-------------|
| `frontend/src/pages/` | Page components (Dashboard, Login, Areas, etc.) |
| `frontend/src/components/` | Reusable UI components (Charts, Cards, Tables) |
| `frontend/src/services/` | API client and authentication service |
| `frontend/src/context/` | React context for state management |

### Pages (Planned)
| Page | Features |
|------|----------|
| Login | Email/password authentication |
| Overview | Total consumption, area comparison, trends |
| Area Detail | Per-area charts and statistics |
| Predictions | AI forecasts with confidence intervals |
| Anomalies | Alert list with severity and details |
| Settings | User profile and preferences |

### Dependencies
- React 18, Vite, Recharts/Chart.js, Axios, React Router

### Implementation Phase
Phase 5

---

## Module 8: Authentication

### Purpose
Secure the system with user authentication and role-based access control.

### Scope
- User registration and login
- JWT token generation and validation
- Password hashing with bcrypt
- Role-based permissions (admin, viewer)
- Token refresh mechanism

### Key Components
| Component | Description |
|-----------|-------------|
| `backend/core/security.py` | JWT creation, verification, password hashing |
| `backend/routers/auth.py` | Authentication API endpoints |
| `backend/models/user.py` | User database model |
| `frontend/src/services/auth.js` | Frontend auth service and token management |

### Security Specifications
| Specification | Value |
|--------------|-------|
| Algorithm | HS256 |
| Token Expiry | 30 minutes (access), 7 days (refresh) |
| Password Hash | bcrypt, 12 rounds |
| Token Storage | httpOnly cookie or localStorage |

### Dependencies
- python-jose, passlib[bcrypt]

### Implementation Phase
Phase 3

---

## Module 9: Security

### Purpose
Implement comprehensive security measures across all layers of the application.

### Scope
- Input validation and sanitization
- CORS configuration
- Rate limiting
- SQL injection prevention
- XSS prevention
- Security headers
- Audit logging

### Key Components
| Component | Description |
|-----------|-------------|
| `backend/core/security.py` | Security utilities and middleware |
| `backend/middleware/` | Rate limiter, CORS, security headers |
| Network ACLs | Traffic filtering (Packet Tracer) |

### Security Checklist
| Category | Measures |
|----------|----------|
| **API Security** | JWT auth, input validation, rate limiting, CORS |
| **Data Security** | bcrypt passwords, parameterized queries, encrypted tokens |
| **Network Security** | VLANs, ACLs, port security, unused port shutdown |
| **Application Security** | Security headers, XSS prevention, CSRF protection |
| **Operational Security** | Logging, error handling, dependency scanning |

### Dependencies
- Integrated across all modules

### Implementation Phase
Phase 7

---

## Module 10: Testing

### Purpose
Ensure system reliability, correctness, and performance through automated and manual testing.

### Scope
- Unit tests for backend functions
- API integration tests
- IoT simulator output validation
- ML model evaluation tests
- Frontend component tests (optional)
- End-to-end workflow tests

### Key Components
| Component | Description |
|-----------|-------------|
| `backend/tests/` | Backend unit and integration tests |
| `ai/tests/` | ML model evaluation tests |
| `iot/tests/` | Simulator output validation |
| `frontend/src/__tests__/` | Frontend component tests |

### Testing Strategy
| Level | Tool | Scope |
|-------|------|-------|
| Unit | pytest | Individual functions and methods |
| Integration | pytest + httpx | API endpoint testing |
| ML Evaluation | scikit-learn metrics | Model accuracy and performance |
| Frontend | React Testing Library | Component rendering and behavior |
| End-to-End | Manual / Selenium (optional) | Full workflow validation |

### Dependencies
- pytest, httpx (for async testing), coverage

### Implementation Phase
Phase 7

---

## Module Dependency Map

```
                    ┌──────────────────┐
                    │  Module 10:      │
                    │  Testing         │ ← Tests all modules
                    └──────────────────┘

┌──────────────┐    ┌──────────────────┐
│  Module 7:   │───→│  Module 3:       │
│  Dashboard   │    │  Backend API     │
└──────────────┘    └───────┬──────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Module 8:   │    │  Module 4:   │    │  Module 5:   │
│  Auth        │    │  Database    │    │  Prediction  │
└──────────────┘    └──────────────┘    └──────────────┘
                            ▲                   
                            │           ┌──────────────┐
                            │           │  Module 6:   │
                    ┌───────┴──────┐    │  Anomaly Det │
                    │  Module 1:   │    └──────────────┘
                    │  IoT Sim     │
                    └──────────────┘

┌──────────────┐    ┌──────────────┐
│  Module 2:   │    │  Module 9:   │
│  Network     │    │  Security    │ ← Cross-cutting
└──────────────┘    └──────────────┘
```

---

## Implementation Timeline

| Phase | Modules | Duration (Estimated) |
|-------|---------|---------------------|
| Phase 1 | Project setup, documentation | Week 1 |
| Phase 2 | Module 1 (IoT Sim), Module 3 (API skeleton), Module 4 (Database) | Weeks 2–3 |
| Phase 3 | Module 3 (API endpoints), Module 8 (Auth) | Week 4 |
| Phase 4 | Module 5 (Prediction), Module 6 (Anomaly Detection) | Weeks 5–6 |
| Phase 5 | Module 7 (Dashboard) | Weeks 7–8 |
| Phase 6 | Module 2 (Network Simulation) | Week 9 |
| Phase 7 | Module 9 (Security), Module 10 (Testing) | Week 10 |
| Phase 8 | Integration, demo, final report | Weeks 11–12 |

---

*Document Version: 1.0 | Created: August 2026*
