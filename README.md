# 🏫 AI-Driven Smart Energy Consumption Monitoring and Prediction System for Smart Campus

> **Gujarat Technological University – Computer Engineering**
> **Subject:** Computer Networks – PBL (Complex Problem Solving Project)

---

## 📋 Project Objective

Design and develop a software-based smart-campus energy monitoring prototype that leverages **Artificial Intelligence**, **IoT simulation**, **Computer Networking**, and **Web Technologies** to monitor, predict, and optimize energy consumption across multiple campus areas.

---

## 🔍 Problem Statement

Educational institutions consume significant amounts of electrical energy across classrooms, laboratories, libraries, and administrative offices. Without a centralized, intelligent monitoring system, energy wastage goes undetected, costs escalate, and sustainability goals remain unmet.

There is a need for an integrated system that can:

1. **Monitor** real-time energy consumption across campus zones.
2. **Predict** future energy demand using machine learning.
3. **Detect anomalies** such as unusual consumption spikes or equipment faults.
4. **Visualize** actionable insights through a web-based dashboard.
5. **Demonstrate** computer networking concepts including VLANs, IP addressing, routing, and secure data transmission.

---

## 🎯 Main Objectives

| # | Objective |
|---|-----------|
| 1 | Simulate IoT-based energy meters for four campus areas using Python |
| 2 | Design a campus network architecture with VLANs, routing, and access control |
| 3 | Build a RESTful backend API using FastAPI with JWT authentication |
| 4 | Store and manage energy data in an SQLite database |
| 5 | Train ML models for energy consumption prediction and anomaly detection |
| 6 | Develop an interactive React-based web dashboard for data visualization |
| 7 | Implement cybersecurity best practices (encryption, authentication, input validation) |
| 8 | Document the complete system architecture and data flow |

---

## 💡 Proposed Solution

The system consists of the following integrated layers:

```
┌─────────────────────────────────────────────────┐
│              Web Dashboard (React + Vite)        │
├─────────────────────────────────────────────────┤
│          AI / ML Layer (Scikit-learn)             │
│       ┌──────────────┬──────────────────┐        │
│       │  Prediction  │ Anomaly Detection │        │
│       └──────────────┴──────────────────┘        │
├─────────────────────────────────────────────────┤
│           Database Layer (SQLite)                 │
├─────────────────────────────────────────────────┤
│       Backend API (FastAPI + JWT Auth)            │
├─────────────────────────────────────────────────┤
│      IoT Gateway / Network Communication         │
├─────────────────────────────────────────────────┤
│    Campus Network (VLANs, Routing, Firewall)     │
├─────────────────────────────────────────────────┤
│     Virtual IoT Energy Meters (Python Sim)       │
└─────────────────────────────────────────────────┘
```

### Data Flow

```
Virtual IoT Energy Meters
        ↓
Campus Network (Simulated)
        ↓
IoT Gateway / Backend API
        ↓
Database (SQLite)
        ↓
AI / ML Engine
   ┌────┴────┐
   ↓         ↓
Prediction  Anomaly Detection
   └────┬────┘
        ↓
Web Dashboard
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Vite, Chart.js / Recharts |
| **Backend** | Python 3.11+, FastAPI, Uvicorn |
| **Database** | SQLite (initial), PostgreSQL (future) |
| **AI / ML** | Scikit-learn, Pandas, NumPy |
| **IoT Simulation** | Python (custom simulator scripts) |
| **Network Simulation** | Cisco Packet Tracer |
| **Authentication** | JWT (JSON Web Tokens) |
| **API Protocol** | REST (MQTT planned for future) |
| **Version Control** | Git + GitHub |
| **Documentation** | Markdown |

---

## 🏗️ High-Level Architecture

The system is organized into **seven layers**, each addressing a specific concern:

1. **IoT Layer** – Python-based virtual energy meters simulating power readings for four campus areas.
2. **Network Layer** – Campus network design with VLANs, IP addressing, and routing (simulated in Cisco Packet Tracer).
3. **Backend Layer** – FastAPI RESTful API serving as the IoT gateway and data processing engine.
4. **Database Layer** – SQLite database storing energy readings, user accounts, and system configuration.
5. **AI/ML Layer** – Scikit-learn models for consumption prediction (regression) and anomaly detection.
6. **Dashboard Layer** – React + Vite single-page application for real-time visualization and reporting.
7. **Security Layer** – JWT authentication, HTTPS, input validation, and role-based access control.

---

## 📅 Development Phases

| Phase | Description | Status |
|-------|-------------|--------|
| **Phase 1** | Project setup, architecture, documentation, folder structure | ✅ In Progress |
| **Phase 2** | IoT simulator development, database schema, backend API skeleton | ⬜ Planned |
| **Phase 3** | Backend API endpoints, data ingestion pipeline, authentication | ⬜ Planned |
| **Phase 4** | AI/ML model training – prediction and anomaly detection | ✅ Completed |
| **Phase 5** | React dashboard development and API integration | ✅ Completed |
| **Phase 6** | Network simulation in Cisco Packet Tracer | ⬜ Planned |
| **Phase 7** | Security hardening, testing, and documentation finalization | ⬜ Planned |
| **Phase 8** | Final integration, demo preparation, and project report | ⬜ Planned |

---

## ⚠️ Important Note: Simulated IoT Data

> **This project uses SIMULATED IoT energy data generated by Python scripts.**
>
> No physical sensors, smart meters, or IoT hardware devices are installed or required for the initial prototype. The IoT simulator generates realistic energy consumption patterns based on:
> - Time-of-day usage profiles
> - Campus area type (lab, classroom, library, office)
> - Weekday vs. weekend variations
> - Random noise for realism
>
> This approach allows the complete system to be developed, tested, and demonstrated **without purchasing any hardware**.

---

## 🔮 Future Hardware Integration

The system architecture is designed to be **hardware-ready**. In future iterations:

- Physical IoT energy meters (e.g., PZEM-004T, INA219) can replace the simulator.
- Microcontrollers (ESP32, Raspberry Pi) can be deployed as IoT gateways.
- MQTT protocol can be integrated for real-time sensor communication.
- The SQLite database can be migrated to PostgreSQL or a cloud database.
- The system can be deployed on AWS / Azure / GCP for production use.

The transition from simulation to physical deployment requires **minimal code changes** due to the modular, layered architecture.

---

## 📂 Project Structure

```
SmartEnergyMonitor/
├── backend/                  # FastAPI backend server
├── frontend/                 # React + Vite dashboard
├── ai/                       # ML models and training scripts
├── iot/                      # IoT simulator scripts
├── network/                  # Cisco Packet Tracer files, network docs
├── docs/                     # Project documentation
│   ├── architecture/         # System, network, and data flow diagrams
│   ├── research/             # Research papers and references
│   └── reports/              # Requirements, module plans, project reports
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

---

## 👨‍💻 Team

| Role | Responsibility |
|------|---------------|
| Full-Stack Developer | Backend API, Frontend Dashboard |
| AI/ML Engineer | Prediction and Anomaly Detection Models |
| Network Engineer | Campus Network Design, Cisco Packet Tracer |
| IoT Developer | Simulator Development, Data Pipeline |

---

## 📜 License

This project is developed for academic purposes as part of the Gujarat Technological University Computer Engineering curriculum.

---

*Last Updated: August 2026*
#   S m a r t E n e r g y M o n i t o r _ C N _ R u d r a  
 