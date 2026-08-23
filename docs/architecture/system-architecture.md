# System Architecture

> AI-Driven Smart Energy Consumption Monitoring and Prediction System for Smart Campus

---

## 1. System Overview

The Smart Energy Monitor is a **multi-layered, modular system** designed to simulate, collect, process, analyze, and visualize energy consumption data across a smart campus environment.

The architecture follows a **layered approach** where each layer has a well-defined responsibility and communicates with adjacent layers through standardized interfaces (REST APIs, database queries, function calls).

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                         │
│              React + Vite Web Dashboard                       │
│         (Charts, Tables, Alerts, Reports)                     │
├──────────────────────────────────────────────────────────────┤
│                    APPLICATION LAYER                          │
│                                                              │
│  ┌──────────────────────┐    ┌───────────────────────────┐   │
│  │   FastAPI Backend     │    │     AI/ML Engine          │   │
│  │   - REST API          │    │   - Prediction Model      │   │
│  │   - JWT Auth          │    │   - Anomaly Detection     │   │
│  │   - Data Validation   │    │   - Data Preprocessing    │   │
│  │   - IoT Gateway       │    │   - Model Serving         │   │
│  └──────────┬───────────┘    └───────────┬───────────────┘   │
│             │                            │                    │
├─────────────┼────────────────────────────┼────────────────────┤
│             │       DATA LAYER           │                    │
│             └──────────┬─────────────────┘                    │
│                        │                                      │
│              ┌─────────▼─────────┐                            │
│              │   SQLite Database  │                            │
│              │   - Energy Data    │                            │
│              │   - User Accounts  │                            │
│              │   - System Config  │                            │
│              │   - ML Results     │                            │
│              └───────────────────┘                            │
├──────────────────────────────────────────────────────────────┤
│                    NETWORK LAYER                              │
│          Campus Network (Simulated in Packet Tracer)          │
│      VLANs │ IP Addressing │ Routing │ ACLs │ Firewall       │
├──────────────────────────────────────────────────────────────┤
│                    PERCEPTION LAYER                            │
│           Virtual IoT Energy Meters (Python)                  │
│                                                              │
│   ┌───────────┐ ┌───────────┐ ┌─────────┐ ┌──────────────┐  │
│   │ Computer  │ │ Classroom │ │ Library │ │ Admin Office │  │
│   │    Lab    │ │           │ │         │ │              │  │
│   └───────────┘ └───────────┘ └─────────┘ └──────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. IoT Layer (Perception Layer)

### Purpose
Simulate energy consumption readings from virtual smart meters installed in four campus areas.

### Components

| Component | Description |
|-----------|-------------|
| **Energy Meter Simulator** | Python script generating realistic energy data |
| **Data Generator** | Creates consumption patterns based on time, area type, and occupancy |
| **Data Formatter** | Structures data into JSON payloads for API transmission |

### Campus Areas Monitored

| Area | Typical Devices | Peak Hours |
|------|----------------|------------|
| Computer Laboratory | Desktops, servers, monitors, AC | 09:00 – 17:00 |
| Classroom | Lights, fans, projectors, AC | 08:00 – 16:00 |
| Library | Lights, computers, AC, charging points | 09:00 – 20:00 |
| Administrative Office | Computers, printers, AC, lights | 09:00 – 18:00 |

### Simulated Data Fields

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `area_id` | String | – | Unique identifier for the campus area |
| `area_name` | String | – | Human-readable area name |
| `timestamp` | ISO 8601 | – | Time of reading |
| `voltage` | Float | Volts (V) | Simulated voltage reading |
| `current` | Float | Amperes (A) | Simulated current reading |
| `power` | Float | Watts (W) | Calculated power consumption |
| `energy` | Float | kWh | Cumulative energy consumed |
| `power_factor` | Float | – | Power factor (0.0 – 1.0) |

### Important Note
> All IoT data is **simulated using Python scripts**. No physical sensors or hardware are deployed. The simulator generates realistic patterns including time-of-day variations, weekday/weekend differences, and random noise.

---

## 3. Network Layer

### Purpose
Design and simulate a campus network infrastructure that would connect physical IoT devices to the backend server in a real deployment.

### Components

| Component | Role |
|-----------|------|
| **IoT Devices** | Virtual energy meters (end devices) |
| **Access Switches** | Connect IoT devices within each building zone |
| **Distribution Switch** | Aggregates traffic from access switches |
| **Core Router** | Routes traffic between VLANs and to the server |
| **Backend Server** | Hosts the FastAPI application and database |
| **Firewall** | Controls traffic flow and enforces security policies |

### Network Design Principles
- **VLAN Segmentation** – Separate IoT traffic from management and user traffic.
- **IP Subnetting** – Organized IPv4 addressing scheme per area.
- **Access Control Lists (ACLs)** – Restrict unauthorized access to IoT and server VLANs.
- **Routing** – Inter-VLAN routing via Layer 3 switch or router.

### Simulation Tool
The network is designed and simulated using **Cisco Packet Tracer**. See [network-architecture.md](network-architecture.md) for detailed network design.

---

## 4. Backend Layer

### Purpose
Serve as the central hub for data ingestion, processing, authentication, and API services.

### Technology
- **Framework:** FastAPI (Python)
- **Server:** Uvicorn (ASGI)
- **Authentication:** JWT (JSON Web Tokens)
- **API Style:** RESTful

### Core Responsibilities

| Responsibility | Description |
|---------------|-------------|
| **IoT Data Ingestion** | Receive energy readings from the IoT simulator via REST API |
| **Data Validation** | Validate and sanitize incoming data |
| **Authentication** | Issue and verify JWT tokens for dashboard access |
| **CRUD Operations** | Create, read, update, delete energy records |
| **AI Integration** | Trigger ML predictions and serve results to the dashboard |
| **Error Handling** | Structured error responses with appropriate HTTP status codes |

### API Endpoint Groups (Planned)

| Group | Base Path | Description |
|-------|-----------|-------------|
| Authentication | `/api/auth/` | Login, register, token refresh |
| Energy Data | `/api/energy/` | Submit and query energy readings |
| Areas | `/api/areas/` | Campus area management |
| Predictions | `/api/predictions/` | ML prediction results |
| Anomalies | `/api/anomalies/` | Anomaly detection alerts |
| Dashboard | `/api/dashboard/` | Aggregated statistics for UI |

---

## 5. Database Layer

### Purpose
Persist all energy data, user information, system configuration, and ML results.

### Technology
- **Initial:** SQLite (file-based, zero-configuration)
- **Future:** PostgreSQL (for production/cloud deployment)

### Key Tables (Planned)

| Table | Purpose |
|-------|---------|
| `users` | User accounts and authentication |
| `campus_areas` | Campus area definitions and metadata |
| `energy_readings` | Raw energy consumption data from IoT simulator |
| `predictions` | ML prediction results |
| `anomalies` | Detected anomaly records |
| `system_config` | Application configuration parameters |

### Design Principles
- Normalized schema design (3NF)
- Indexed columns for frequent queries (timestamp, area_id)
- Foreign key constraints for data integrity
- Timestamps in UTC for consistency

---

## 6. AI/ML Layer

### Purpose
Analyze historical energy data to predict future consumption and detect anomalous patterns.

### Technology
- **Library:** Scikit-learn
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib (for training analysis)

### Models

#### 6.1 Energy Consumption Prediction
| Aspect | Detail |
|--------|--------|
| **Type** | Supervised Learning – Regression |
| **Goal** | Predict energy consumption for the next hour/day |
| **Input Features** | Time of day, day of week, area type, historical consumption |
| **Candidate Algorithms** | Linear Regression, Random Forest Regressor, Gradient Boosting |
| **Output** | Predicted energy consumption (kWh) |

#### 6.2 Anomaly Detection
| Aspect | Detail |
|--------|--------|
| **Type** | Unsupervised / Semi-supervised Learning |
| **Goal** | Identify unusual consumption patterns |
| **Input Features** | Current reading vs. historical baseline |
| **Candidate Algorithms** | Isolation Forest, One-Class SVM, Statistical Z-Score |
| **Output** | Anomaly flag, severity score, description |

### ML Pipeline (Planned)
```
Raw Data → Preprocessing → Feature Engineering → Model Training → Evaluation → Deployment
```

---

## 7. Dashboard Layer

### Purpose
Provide a visual, interactive interface for campus administrators to monitor energy consumption, view predictions, and receive anomaly alerts.

### Technology
- **Framework:** React 18
- **Build Tool:** Vite
- **Charts:** Chart.js or Recharts
- **HTTP Client:** Axios or Fetch API
- **State Management:** React Context API or Zustand

### Dashboard Pages (Planned)

| Page | Features |
|------|----------|
| **Login** | JWT-based authentication |
| **Overview** | Total consumption, area comparison, trend summary |
| **Area Detail** | Per-area consumption charts, historical data |
| **Predictions** | AI-predicted consumption for upcoming periods |
| **Anomalies** | Alert list, severity indicators, details |
| **Reports** | Downloadable reports, date-range filtering |
| **Settings** | User profile, system configuration |

---

## 8. Cybersecurity Layer

### Purpose
Protect the system against unauthorized access, data tampering, and common web vulnerabilities.

### Security Measures

| Measure | Implementation |
|---------|---------------|
| **Authentication** | JWT tokens with expiration and refresh mechanism |
| **Password Security** | Bcrypt hashing, minimum complexity requirements |
| **Input Validation** | Pydantic models for all API inputs |
| **CORS** | Configured to allow only trusted origins |
| **HTTPS** | TLS encryption for all API communications (production) |
| **Rate Limiting** | Throttle API requests to prevent abuse |
| **SQL Injection Prevention** | Parameterized queries via ORM |
| **XSS Prevention** | React's built-in escaping, Content-Security-Policy headers |
| **Role-Based Access** | Admin vs. viewer roles with different permissions |
| **Logging** | Audit logs for authentication events and data access |

---

## 9. Data Flow Summary

```
[1] IoT Simulator generates energy reading (JSON)
            │
            ▼
[2] HTTP POST request to Backend API
            │
            ▼
[3] FastAPI validates and processes the data
            │
            ▼
[4] Data stored in SQLite database
            │
            ▼
[5] AI/ML models analyze historical data
        ┌───┴───┐
        ▼       ▼
[6a] Prediction [6b] Anomaly Detection
        └───┬───┘
            ▼
[7] Results stored in database
            │
            ▼
[8] Dashboard fetches data via REST API
            │
            ▼
[9] React renders charts, tables, and alerts
```

---

## 10. Deployment Architecture (Future)

```
┌─────────────────────────────────────────┐
│              Cloud (AWS / Azure)          │
│                                          │
│  ┌──────────┐  ┌───────────────────┐     │
│  │ Frontend  │  │  Backend (EC2/    │     │
│  │ (S3 +    │  │  App Service)     │     │
│  │ CloudFront)│  │  + AI Models     │     │
│  └──────────┘  └───────┬───────────┘     │
│                        │                  │
│              ┌─────────▼─────────┐       │
│              │  PostgreSQL (RDS) │       │
│              └───────────────────┘       │
└─────────────────────────────────────────┘
```

> Cloud deployment is planned for future phases. The initial prototype runs entirely on localhost.

---

*Document Version: 1.0 | Created: August 2026*
