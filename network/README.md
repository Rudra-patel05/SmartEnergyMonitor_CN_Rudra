# 🌐 Campus Network Architecture Module

> **Smart Campus Energy Monitoring & Prediction System (GTU PBL)**  
> **Module:** `network/` — Campus Network Design, VLAN Segmentation, Inter-VLAN Routing & Cisco ACLs  
> **Status:** Day 11 & Day 12 Complete ✅

---

## 1. Overview & Objectives

The `network/` module provides the Computer Networking foundation for the Smart Campus Energy platform. It models an isolated, secure enterprise campus network connecting virtual IoT meters, core routing infrastructure, servers, and user workstations.

```
                  ┌─────────────────────────────────────┐
                  │    Core Router (R1) — ROAS Gateway  │
                  └──────────────────┬──────────────────┘
                                     │ 802.1Q Trunk
                  ┌──────────────────┴──────────────────┐
                  │       Core Switch (SW-CORE-01)      │
                  └─────────┬─────────────────┬─────────┘
                            │                 │
              ┌─────────────┴─────┐     ┌─────┴─────────────┐
              │ SW-ACC-01 (IoT 1) │     │ SW-ACC-02 (IoT 2) │
              └───────┬─────┬─────┘     └───────┬─────┬─────┘
                      │     │                   │     │
                 [VLAN 10][VLAN 20]        [VLAN 30][VLAN 40]
                  Lab IoT  Class IoT        Lib/Adm   Users
```

---

## 2. Directory Structure

```
network/
├── README.md                                  # Main Network module overview
├── topology/
│   ├── topology_specification.md              # Topology specification, cabling & setup guide
│   └── cisco_ios_configs.md                   # Ready-to-paste Cisco IOS commands for Router & Switches
└── documentation/
    ├── ip-addressing.md                       # Comprehensive IPv4 subnetting & device IP plan
    ├── vlan-design.md                         # VLAN allocation matrix, trunking & port security
    ├── routing-design.md                      # Router-on-a-Stick, sub-interfaces & routing flows
    └── security-rules.md                      # Extended ACLs, zero-trust rules & traffic isolation
```

---

## 3. Network Architecture Summary

### 3.1. VLAN Allocation & Subnets

| VLAN ID | Segment Name | Network / CIDR | Default Gateway | Primary Endpoints |
| :---: | :--- | :--- | :--- | :--- |
| **10** | **LAB IoT** | `192.168.10.0/24` | `192.168.10.1` | Computer Lab Meters (`LAB-01`, `LAB-02`) |
| **20** | **CLASSROOM IoT** | `192.168.20.0/24` | `192.168.20.1` | Classroom Meters (`CLASS-01`, `CLASS-02`) |
| **30** | **LIB / ADMIN IoT**| `192.168.30.0/24` | `192.168.30.1` | Library & Admin Office Meters (`LIB-01`, `ADMIN-01`)|
| **40** | **USERS** | `192.168.40.0/24` | `192.168.40.1` | Faculty PCs & Student Dashboard Clients |
| **50** | **SERVERS** | `192.168.50.0/24` | `192.168.50.1` | FastAPI Backend (`.10`), React Frontend (`.20`) |
| **99** | **MANAGEMENT** | `192.168.99.0/24` | `192.168.99.1` | Switch SVI Management & Native VLAN |

### 3.2. Routing & Security Features
- **Router-on-a-Stick (ROAS):** Core Router `R1` multiplexes traffic across sub-interfaces `Gig0/0.10` through `Gig0/0.50` with 802.1Q encapsulation.
- **Traffic Isolation:** IoT VLANs are isolated from each other and cannot access User subnets.
- **Controlled Ingestion:** IoT meters are restricted to sending HTTP traffic solely to Backend Server (`192.168.50.10:8000`).

---

## 4. Packet Tracer Setup & Simulation Guide

To simulate the smart campus network in Cisco Packet Tracer:
1. Open Cisco Packet Tracer 8.x.
2. Follow the topology layout and cabling detailed in [`topology/topology_specification.md`](topology/topology_specification.md).
3. Copy-paste the Cisco IOS scripts from [`topology/cisco_ios_configs.md`](topology/cisco_ios_configs.md) into the CLI tab of each corresponding switch and router.
4. Perform ICMP ping and ACL verification tests as documented.
