# 🌐 IPv4 Addressing Scheme — Smart Campus Network

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Network Architecture & Computer Networks (Day 11)  
> **Institution:** Gujarat Technological University – Computer Engineering

---

## 1. Overview & Disclaimer

> [!NOTE]
> The IPv4 addressing scheme presented below is a **simulated prototype network architecture** designed for the academic Computer Networks PBL project. These private addresses (`RFC 1918`) model an isolated smart-campus enterprise network and do not claim to represent live institutional public infrastructure.

The network uses Class C private IPv4 addresses with `/24` subnets (Subnet Mask `255.255.255.0`), allowing up to 254 usable host IP addresses per VLAN segment.

---

## 2. IPv4 Subnet Allocation Table

| VLAN ID | Segment Name | Network Address | Subnet Mask | Usable Host Range | Default Gateway | Purpose |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **VLAN 10** | **LAB IoT** | `192.168.10.0/24` | `255.255.255.0` | `192.168.10.2` – `192.168.10.254` | `192.168.10.1` | Computer Labs 1 & 2 Energy Meters (LAB-01, LAB-02) |
| **VLAN 20** | **CLASSROOM IoT** | `192.168.20.0/24` | `255.255.255.0` | `192.168.20.2` – `192.168.20.254` | `192.168.20.1` | Classrooms 101 & 102 Meters (CLASS-01, CLASS-02) |
| **VLAN 30** | **LIB / ADMIN IoT** | `192.168.30.0/24` | `255.255.255.0` | `192.168.30.2` – `192.168.30.254` | `192.168.30.1` | Library & Admin Office Meters (LIB-01, ADMIN-01) |
| **VLAN 40** | **USERS** | `192.168.40.0/24` | `255.255.255.0` | `192.168.40.2` – `192.168.40.254` | `192.168.40.1` | Faculty workstations, student lab PCs, operators |
| **VLAN 50** | **BACKEND / SERVERS**| `192.168.50.0/24` | `255.255.255.0` | `192.168.50.2` – `192.168.50.254` | `192.168.50.1` | FastAPI Gateway, SQLite DB, ML Engine, React Server |
| **VLAN 99** | **MANAGEMENT** | `192.168.99.0/24` | `255.255.255.0` | `192.168.99.2` – `192.168.99.254` | `192.168.99.1` | Switch SVI Management & Router OOB Access |

---

## 3. Dedicated Device IP Allocation

### 3.1. Infrastructure & Server Nodes

| Device Name | Function | Interface / SVI | Assigned IP | Subnet Mask | Gateway |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R1 (Core Router)** | Default Gateway | `Gig0/0.10` | `192.168.10.1` | `255.255.255.0` | N/A |
| **R1 (Core Router)** | Default Gateway | `Gig0/0.20` | `192.168.20.1` | `255.255.255.0` | N/A |
| **R1 (Core Router)** | Default Gateway | `Gig0/0.30` | `192.168.30.1` | `255.255.255.0` | N/A |
| **R1 (Core Router)** | Default Gateway | `Gig0/0.40` | `192.168.40.1` | `255.255.255.0` | N/A |
| **R1 (Core Router)** | Default Gateway | `Gig0/0.50` | `192.168.50.1` | `255.255.255.0` | N/A |
| **R1 (Core Router)** | Default Gateway | `Gig0/0.99` | `192.168.99.1` | `255.255.255.0` | N/A |
| **SW-CORE-01** | Core Distribution Switch | `VLAN 99 SVI` | `192.168.99.2` | `255.255.255.0` | `192.168.99.1` |
| **SW-ACC-01 (IoT)**| Access Switch 1 (Labs/Classes) | `VLAN 99 SVI` | `192.168.99.11` | `255.255.255.0` | `192.168.99.1` |
| **SW-ACC-02 (Users)**| Access Switch 2 (Admin/Users) | `VLAN 99 SVI` | `192.168.99.12` | `255.255.255.0` | `192.168.99.1` |
| **SRV-BACKEND-01** | FastAPI Backend & ML Engine | `Eth0` | `192.168.50.10` | `255.255.255.0` | `192.168.50.1` |
| **SRV-FRONTEND-01** | Web Dashboard (React/Vite) | `Eth0` | `192.168.50.20` | `255.255.255.0` | `192.168.50.1` |

### 3.2. Simulated IoT Energy Meter Nodes

| Meter ID | Location Description | VLAN | Assigned IP | Subnet Mask | Default Gateway |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `LAB-01` | Computer Laboratory 1 | 10 | `192.168.10.10` | `255.255.255.0` | `192.168.10.1` |
| `LAB-02` | Computer Laboratory 2 | 10 | `192.168.10.11` | `255.255.255.0` | `192.168.10.1` |
| `CLASS-01` | Smart Classroom 101 | 20 | `192.168.20.10` | `255.255.255.0` | `192.168.20.1` |
| `CLASS-02` | Smart Classroom 102 | 20 | `192.168.20.11` | `255.255.255.0` | `192.168.20.1` |
| `LIB-01` | Central Campus Library | 30 | `192.168.30.10` | `255.255.255.0` | `192.168.30.1` |
| `ADMIN-01` | Administrative Building Office | 30 | `192.168.30.20` | `255.255.255.0` | `192.168.30.1` |

---

## 4. DHCP vs. Static Allocation Strategy

1. **Static IP Configuration:**
   - All IoT Energy Meters, Gateways, Core Routers, Switches, and Backend Servers are statically addressed to ensure deterministic DNS/routing mapping and strict ACL enforcement.
2. **Dynamic DHCP Pool (Optional for VLAN 40):**
   - VLAN 40 (User Workstations & Laptops) can optionally obtain IP addresses dynamically via DHCP pool configured on Core Router R1 (`192.168.40.100` – `192.168.40.200`).
