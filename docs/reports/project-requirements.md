# Project Requirements Document

> AI-Driven Smart Energy Consumption Monitoring and Prediction System for Smart Campus

---

## 1. Functional Requirements

### FR-01: IoT Data Simulation
| ID | Requirement |
|----|------------|
| FR-01.1 | The system shall simulate energy consumption data for four campus areas: Computer Laboratory, Classroom, Library, and Administrative Office. |
| FR-01.2 | The simulator shall generate readings at configurable intervals (default: 60 seconds). |
| FR-01.3 | Simulated data shall include voltage, current, power, energy, and power factor. |
| FR-01.4 | Data patterns shall vary based on time of day, day of week, and area type. |
| FR-01.5 | The simulator shall add realistic random noise to the generated data. |

### FR-02: Backend API
| ID | Requirement |
|----|------------|
| FR-02.1 | The backend shall provide RESTful API endpoints for data ingestion, retrieval, and management. |
| FR-02.2 | The API shall validate all incoming data against predefined schemas. |
| FR-02.3 | The API shall support pagination for large data queries. |
| FR-02.4 | The API shall return appropriate HTTP status codes and error messages. |
| FR-02.5 | The API shall support filtering by campus area, date range, and time period. |

### FR-03: Authentication and Authorization
| ID | Requirement |
|----|------------|
| FR-03.1 | The system shall support user registration with email and password. |
| FR-03.2 | The system shall authenticate users using JWT tokens. |
| FR-03.3 | JWT tokens shall have a configurable expiration time. |
| FR-03.4 | The system shall support role-based access control (admin, viewer). |
| FR-03.5 | Passwords shall be hashed using bcrypt before storage. |

### FR-04: Database
| ID | Requirement |
|----|------------|
| FR-04.1 | The system shall store all energy readings in a persistent database. |
| FR-04.2 | The database shall support querying by area, time range, and reading type. |
| FR-04.3 | The database shall maintain referential integrity between related tables. |
| FR-04.4 | The system shall support data export for analysis purposes. |

### FR-05: AI/ML – Energy Prediction
| ID | Requirement |
|----|------------|
| FR-05.1 | The system shall predict energy consumption for the next 1-hour and 24-hour periods. |
| FR-05.2 | Predictions shall be generated per campus area. |
| FR-05.3 | The system shall display prediction accuracy metrics (MAE, RMSE, R²). |
| FR-05.4 | The prediction model shall be re-trainable with new data. |

### FR-06: AI/ML – Anomaly Detection
| ID | Requirement |
|----|------------|
| FR-06.1 | The system shall detect anomalous energy consumption patterns. |
| FR-06.2 | Anomalies shall be classified by severity (low, medium, high). |
| FR-06.3 | The system shall provide a description and possible cause for each anomaly. |
| FR-06.4 | Anomaly alerts shall be visible on the dashboard. |

### FR-07: Web Dashboard
| ID | Requirement |
|----|------------|
| FR-07.1 | The dashboard shall display real-time energy consumption for all campus areas. |
| FR-07.2 | The dashboard shall show historical consumption trends via line charts. |
| FR-07.3 | The dashboard shall display AI predictions with confidence intervals. |
| FR-07.4 | The dashboard shall show anomaly alerts with severity indicators. |
| FR-07.5 | The dashboard shall support date-range filtering and area selection. |
| FR-07.6 | The dashboard shall be responsive and work on desktop and tablet screens. |

### FR-08: Network Simulation
| ID | Requirement |
|----|------------|
| FR-08.1 | A campus network shall be designed and simulated in Cisco Packet Tracer. |
| FR-08.2 | The network design shall include VLANs for traffic segmentation. |
| FR-08.3 | Inter-VLAN routing shall be configured for cross-segment communication. |
| FR-08.4 | ACLs shall be configured to restrict unauthorized traffic. |

---

## 2. Non-Functional Requirements

### NFR-01: Performance
| ID | Requirement |
|----|------------|
| NFR-01.1 | API response time shall be under 500ms for standard queries. |
| NFR-01.2 | The dashboard shall load within 3 seconds on a standard connection. |
| NFR-01.3 | The system shall handle at least 100 concurrent API requests. |

### NFR-02: Security
| ID | Requirement |
|----|------------|
| NFR-02.1 | All API endpoints (except login/register) shall require JWT authentication. |
| NFR-02.2 | All passwords shall be stored using bcrypt hashing (minimum 12 rounds). |
| NFR-02.3 | Input validation shall prevent SQL injection and XSS attacks. |
| NFR-02.4 | CORS shall be configured to allow only trusted origins. |
| NFR-02.5 | API rate limiting shall be implemented to prevent abuse. |

### NFR-03: Reliability
| ID | Requirement |
|----|------------|
| NFR-03.1 | The system shall handle invalid data gracefully without crashing. |
| NFR-03.2 | Database operations shall use transactions for data integrity. |
| NFR-03.3 | The system shall log errors for debugging and audit purposes. |

### NFR-04: Scalability
| ID | Requirement |
|----|------------|
| NFR-04.1 | The architecture shall support migration from SQLite to PostgreSQL. |
| NFR-04.2 | The system shall support adding new campus areas without code changes. |
| NFR-04.3 | The architecture shall support cloud deployment (AWS/Azure/GCP). |

### NFR-05: Maintainability
| ID | Requirement |
|----|------------|
| NFR-05.1 | Code shall follow PEP 8 (Python) and ESLint (JavaScript) standards. |
| NFR-05.2 | All modules shall have clear documentation and docstrings. |
| NFR-05.3 | The project shall use Git for version control with meaningful commit messages. |

### NFR-06: Usability
| ID | Requirement |
|----|------------|
| NFR-06.1 | The dashboard UI shall be intuitive and require no training to use. |
| NFR-06.2 | Error messages shall be user-friendly and actionable. |
| NFR-06.3 | The system shall provide visual feedback for loading and processing states. |

---

## 3. Hardware Requirements

### Development Environment

| Component | Minimum Specification |
|-----------|----------------------|
| **Processor** | Intel Core i3 / AMD Ryzen 3 or equivalent |
| **RAM** | 4 GB (8 GB recommended) |
| **Storage** | 10 GB free disk space |
| **Display** | 1366 × 768 resolution |
| **OS** | Windows 10/11, macOS, or Ubuntu 20.04+ |
| **Network** | Internet connection for package installation |

### Production (Future)

| Component | Specification |
|-----------|--------------|
| **Cloud Server** | AWS EC2 t2.micro or equivalent |
| **Storage** | 20 GB SSD |
| **Network** | Public IP with HTTPS |

> **Note:** The initial prototype runs entirely on a developer's local machine. No specialized hardware is required.

---

## 4. Software Requirements

### Development Tools

| Software | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.11+ | Backend, IoT simulator, AI/ML |
| **Node.js** | 18+ | Frontend build tools |
| **npm** | 9+ | JavaScript package management |
| **Git** | 2.40+ | Version control |
| **Cisco Packet Tracer** | 8.0+ | Network simulation |
| **VS Code** | Latest | Code editor (recommended) |

### Backend Dependencies (to be installed in Phase 2)

| Package | Purpose |
|---------|---------|
| FastAPI | Web framework |
| Uvicorn | ASGI server |
| SQLAlchemy | ORM / database toolkit |
| Pydantic | Data validation |
| python-jose | JWT token handling |
| passlib[bcrypt] | Password hashing |
| scikit-learn | Machine learning |
| pandas | Data manipulation |
| numpy | Numerical computing |

### Frontend Dependencies (to be installed in Phase 5)

| Package | Purpose |
|---------|---------|
| React | UI library |
| Vite | Build tool |
| Recharts / Chart.js | Data visualization |
| Axios | HTTP client |
| React Router | Client-side routing |

---

## 5. Constraints

| # | Constraint |
|---|-----------|
| C-01 | The initial prototype must work **without physical IoT hardware**. |
| C-02 | SQLite is used for the initial version due to zero-configuration setup. |
| C-03 | The project must be completable within one academic semester. |
| C-04 | All tools and libraries must be free and open-source. |
| C-05 | The network simulation is limited to Cisco Packet Tracer capabilities. |
| C-06 | The system is a prototype and is not intended for production deployment. |
| C-07 | The AI models will be trained on simulated data, not real campus data. |
| C-08 | The project must demonstrate Computer Networks concepts (VLANs, routing, ACLs, IP addressing). |

---

## 6. Assumptions

| # | Assumption |
|---|-----------|
| A-01 | The development machine has Python 3.11+ and Node.js 18+ installed. |
| A-02 | Cisco Packet Tracer is available for network simulation. |
| A-03 | Simulated energy data patterns are sufficient to demonstrate ML capabilities. |
| A-04 | The campus has four primary areas for energy monitoring. |
| A-05 | A standard Indian electrical system (230V, 50Hz) is assumed for simulation. |
| A-06 | Internet connectivity is available for downloading packages and dependencies. |
| A-07 | The project team has basic knowledge of Python, JavaScript, and networking. |
| A-08 | Git/GitHub is used for version control and collaboration. |
| A-09 | The initial prototype runs on localhost without cloud deployment. |

---

*Document Version: 1.0 | Created: August 2026*
