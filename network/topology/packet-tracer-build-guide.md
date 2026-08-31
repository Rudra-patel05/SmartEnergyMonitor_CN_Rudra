# 📘 Cisco Packet Tracer Build Plan & Specification Guide

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Network Architecture & Computer Networks (Day 11 & Day 12)  
> **Simulation Platform:** Cisco Packet Tracer 8.x+ (Standalone / Lab Environment)  
> **Status:** Production Specification & Manual Build Reference

---

## 1. Executive Summary & Build Architecture

This document provides a comprehensive, rigorous hardware and logical build plan for the **Smart Energy Campus Network** in Cisco Packet Tracer. The network integrates **14 discrete nodes** organized into a hierarchical design (Core Router $\rightarrow$ Core Distribution Switch $\rightarrow$ Access Switches $\rightarrow$ End Devices / Server Farm).

```
                            [ Router R1 (2911) ]
                                     │ (Gig0/0)
                                     │ Copper Straight-Through
                                     │ (Gig0/1)
                        [ Core Switch SW-CORE-01 (2960) ]
                        ┌────────────┴────────────┐
             (Gig0/2)   │                         │ (Gig0/3)
      ┌─────────────────┘                         └─────────────────┐
      │ (Gig0/1)                                                    │ (Gig0/1)
[ SW-ACC-01 (2960) ]                                          [ SW-ACC-02 (2960) ]
  ├── Fa0/1: LAB-01 (VLAN 10)                                   ├── Fa0/1: LIB-01 (VLAN 30)
  ├── Fa0/2: LAB-02 (VLAN 10)                                   ├── Fa0/2: ADMIN-01 (VLAN 30)
  ├── Fa0/3: CLASS-01 (VLAN 20)                                 ├── Fa0/3: PC_FACULTY_01 (VLAN 40)
  └── Fa0/4: CLASS-02 (VLAN 20)                                 └── Fa0/4: PC_STUDENT_01 (VLAN 40)
                                  [ Server Farm ]
                       (Connected to SW-CORE-01 Access Ports)
                         ├── Fa0/1: SRV_BACKEND_01 (VLAN 50)
                         └── Fa0/2: SRV_FRONTEND_01 (VLAN 50)
```

---

## 2. Bill of Materials (Exact Device Inventory)

| Item # | Device Model (Packet Tracer) | Exact Display Label | Hostname (IOS) | Role / Function |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Router 2911** (or 4321 / 2811) | `R1_CORE_ROUTER` | `R1_CORE_ROUTER` | Inter-VLAN Core Router (Router-on-a-Stick) & ACL Gateway |
| 2 | **Switch 2960-24TT** | `SW_CORE_01` | `SW_CORE_01` | Core Distribution Switch & Server Farm Aggregator |
| 3 | **Switch 2960-24TT** | `SW_ACC_01` | `SW_ACC_01` | Access Switch 1 (Computer Labs & Classrooms) |
| 4 | **Switch 2960-24TT** | `SW_ACC_02` | `SW_ACC_02` | Access Switch 2 (Library, Admin Office & Users) |
| 5 | **Server-PT** | `SRV_BACKEND_01` | `SRV_BACKEND_01` | FastAPI Telemetry Gateway & ML Inference Server |
| 6 | **Server-PT** (or PC-PT) | `SRV_FRONTEND_01` | `SRV_FRONTEND_01` | React Dashboard & Web Client Host |
| 7 | **PC-PT** (or IoT-PT) | `LAB-01` | `LAB-01` | Computer Lab 1 Energy Meter |
| 8 | **PC-PT** (or IoT-PT) | `LAB-02` | `LAB-02` | Computer Lab 2 Energy Meter |
| 9 | **PC-PT** (or IoT-PT) | `CLASS-01` | `CLASS-01` | Classroom 101 Energy Meter |
| 10 | **PC-PT** (or IoT-PT) | `CLASS-02` | `CLASS-02` | Classroom 102 Energy Meter |
| 11 | **PC-PT** (or IoT-PT) | `LIB-01` | `LIB-01` | Central Library Energy Meter |
| 12 | **PC-PT** (or IoT-PT) | `ADMIN-01` | `ADMIN-01` | Administrative Office Energy Meter |
| 13 | **PC-PT** | `PC_FACULTY_01` | `PC_FACULTY_01` | Faculty Workstation (Monitoring Client) |
| 14 | **Laptop-PT** | `PC_STUDENT_01` | `PC_STUDENT_01` | Student / Lab Operator Terminal |

---

## 3. Physical Port & Cabling Matrix

> **Note on Cable Selection in Packet Tracer:**  
> - Between Switch and Router: **Copper Straight-Through** (Cisco Auto-MDIX operates seamlessly, Straight-Through is standard for router-to-switch links).
> - Between Switch and Switch: **Copper Straight-Through** or **Copper Cross-Over** (Auto-MDIX handles both; Cross-Over is traditional L2-to-L2).
> - Between Switch and End Host / Server: **Copper Straight-Through**.

| Source Device | Source Port | Target Device | Target Port | Cable Type | Link Mode / VLAN |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `R1_CORE_ROUTER` | `GigabitEthernet0/0` | `SW_CORE_01` | `GigabitEthernet0/1` | Copper Straight-Through | 802.1Q Trunk (Native 99) |
| `SW_CORE_01` | `GigabitEthernet0/2` | `SW_ACC_01` | `GigabitEthernet0/1` | Copper Cross-Over / Straight | 802.1Q Trunk (Native 99) |
| `SW_CORE_01` | `GigabitEthernet0/3` | `SW_ACC_02` | `GigabitEthernet0/1` | Copper Cross-Over / Straight | 802.1Q Trunk (Native 99) |
| `SW_CORE_01` | `FastEthernet0/1` | `SRV_BACKEND_01` | `FastEthernet0` | Copper Straight-Through | Access — VLAN 50 |
| `SW_CORE_01` | `FastEthernet0/2` | `SRV_FRONTEND_01` | `FastEthernet0` | Copper Straight-Through | Access — VLAN 50 |
| `SW_ACC_01` | `FastEthernet0/1` | `LAB-01` | `FastEthernet0` | Copper Straight-Through | Access — VLAN 10 |
| `SW_ACC_01` | `FastEthernet0/2` | `LAB-02` | `FastEthernet0` | Copper Straight-Through | Access — VLAN 10 |
| `SW_ACC_01` | `FastEthernet0/3` | `CLASS-01` | `FastEthernet0` | Copper Straight-Through | Access — VLAN 20 |
| `SW_ACC_01` | `FastEthernet0/4` | `CLASS-02` | `FastEthernet0` | Copper Straight-Through | Access — VLAN 20 |
| `SW_ACC_02` | `FastEthernet0/1` | `LIB-01` | `FastEthernet0` | Copper Straight-Through | Access — VLAN 30 |
| `SW_ACC_02` | `FastEthernet0/2` | `ADMIN-01` | `FastEthernet0` | Copper Straight-Through | Access — VLAN 30 |
| `SW_ACC_02` | `FastEthernet0/3` | `PC_FACULTY_01` | `FastEthernet0` | Copper Straight-Through | Access — VLAN 40 |
| `SW_ACC_02` | `FastEthernet0/4` | `PC_STUDENT_01` | `FastEthernet0` | Copper Straight-Through | Access — VLAN 40 |

---

## 4. Logical VLAN & Subnet Architecture

| VLAN ID | VLAN Name | Subnet Network | Subnet Mask | Usable Range | Default Gateway | Function |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **10** | `VLAN_LAB_IOT` | `192.168.10.0/24` | `255.255.255.0` | `.2` – `.254` | `192.168.10.1` | Computer Lab 1 & 2 Energy Meters |
| **20** | `VLAN_CLASS_IOT` | `192.168.20.0/24` | `255.255.255.0` | `.2` – `.254` | `192.168.20.1` | Classrooms 101 & 102 Meters |
| **30** | `VLAN_LIB_ADMIN_IOT` | `192.168.30.0/24` | `255.255.255.0` | `.2` – `.254` | `192.168.30.1` | Central Library & Admin Office Meters |
| **40** | `VLAN_USERS` | `192.168.40.0/24` | `255.255.255.0` | `.2` – `.254` | `192.168.40.1` | Faculty & Student Workstations |
| **50** | `VLAN_SERVERS` | `192.168.50.0/24` | `255.255.255.0` | `.2` – `.254` | `192.168.50.1` | FastAPI, ML Engine, React Dashboard Server |
| **99** | `VLAN_MANAGEMENT` | `192.168.99.0/24` | `255.255.255.0` | `.2` – `.254` | `192.168.99.1` | Switch SVIs & Router Native Trunk VLAN |

---

## 5. Complete Static IP Allocation Plan

### 5.1. Endpoints & Server Farm

| Device Name | VLAN | Interface | IP Address | Subnet Mask | Default Gateway | DNS Server |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| `SRV_BACKEND_01` | 50 | `FastEthernet0` | `192.168.50.10` | `255.255.255.0` | `192.168.50.1` | `192.168.50.1` |
| `SRV_FRONTEND_01`| 50 | `FastEthernet0` | `192.168.50.20` | `255.255.255.0` | `192.168.50.1` | `192.168.50.1` |
| `LAB-01` | 10 | `FastEthernet0` | `192.168.10.10` | `255.255.255.0` | `192.168.10.1` | `192.168.50.1` |
| `LAB-02` | 10 | `FastEthernet0` | `192.168.10.11` | `255.255.255.0` | `192.168.10.1` | `192.168.50.1` |
| `CLASS-01` | 20 | `FastEthernet0` | `192.168.20.10` | `255.255.255.0` | `192.168.20.1` | `192.168.50.1` |
| `CLASS-02` | 20 | `FastEthernet0` | `192.168.20.11` | `255.255.255.0` | `192.168.20.1` | `192.168.50.1` |
| `LIB-01` | 30 | `FastEthernet0` | `192.168.30.10` | `255.255.255.0` | `192.168.30.1` | `192.168.50.1` |
| `ADMIN-01` | 30 | `FastEthernet0` | `192.168.30.20` | `255.255.255.0` | `192.168.30.1` | `192.168.50.1` |
| `PC_FACULTY_01` | 40 | `FastEthernet0` | `192.168.40.10` | `255.255.255.0` | `192.168.40.1` | `192.168.50.1` |
| `PC_STUDENT_01` | 40 | `FastEthernet0` | `192.168.40.11` | `255.255.255.0` | `192.168.40.1` | `192.168.50.1` |

### 5.2. Network Infrastructure (SVIs & Router Subinterfaces)

| Device | Interface / SVI | Encapsulation | IP Address | Subnet Mask | Default Gateway |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `R1_CORE_ROUTER` | `Gig0/0.10` | `dot1Q 10` | `192.168.10.1` | `255.255.255.0` | N/A |
| `R1_CORE_ROUTER` | `Gig0/0.20` | `dot1Q 20` | `192.168.20.1` | `255.255.255.0` | N/A |
| `R1_CORE_ROUTER` | `Gig0/0.30` | `dot1Q 30` | `192.168.30.1` | `255.255.255.0` | N/A |
| `R1_CORE_ROUTER` | `Gig0/0.40` | `dot1Q 40` | `192.168.40.1` | `255.255.255.0` | N/A |
| `R1_CORE_ROUTER` | `Gig0/0.50` | `dot1Q 50` | `192.168.50.1` | `255.255.255.0` | N/A |
| `R1_CORE_ROUTER` | `Gig0/0.99` | `dot1Q 99 native` | `192.168.99.1` | `255.255.255.0` | N/A |
| `SW_CORE_01` | `Vlan 99` | SVI | `192.168.99.2` | `255.255.255.0` | `192.168.99.1` |
| `SW_ACC_01` | `Vlan 99` | SVI | `192.168.99.11` | `255.255.255.0` | `192.168.99.1` |
| `SW_ACC_02` | `Vlan 99` | SVI | `192.168.99.12` | `255.255.255.0` | `192.168.99.1` |

---

## 6. Trunk Port Configuration Specifications

1. **`SW_CORE_01` Trunk Ports:**
   - `Gig0/1` $\rightarrow$ Uplink to `R1_CORE_ROUTER Gig0/0`: Native VLAN 99, Allowed VLANs: `10,20,30,40,50,99`.
   - `Gig0/2` $\rightarrow$ Downlink to `SW_ACC_01 Gig0/1`: Native VLAN 99, Allowed VLANs: `10,20,99`.
   - `Gig0/3` $\rightarrow$ Downlink to `SW_ACC_02 Gig0/1`: Native VLAN 99, Allowed VLANs: `30,40,99`.

2. **`SW_ACC_01` Trunk Uplink:**
   - `Gig0/1` $\rightarrow$ Uplink to `SW_CORE_01 Gig0/2`: Native VLAN 99, Allowed VLANs: `10,20,99`.

3. **`SW_ACC_02` Trunk Uplink:**
   - `Gig0/1` $\rightarrow$ Uplink to `SW_CORE_01 Gig0/3`: Native VLAN 99, Allowed VLANs: `30,40,99`.

---

## 7. Access Control List (ACL) Placement & Ordering Specification

> [!IMPORTANT]
> **Cisco Extended ACL Rule Ordering:**  
> Cisco IOS matches extended ACL entries strictly **top-to-bottom on a first-match basis**.  
> To prevent unintentional access, **specific deny statements** (such as lateral cross-VLAN blocks) must appear **BEFORE** any broad permit statements (such as `permit icmp any` or generic network permits).

### 7.1. Placement Table

| ACL Name | Bound Interface | Direction | Protected VLAN / Source | Enforced Security Policies |
| :--- | :--- | :---: | :--- | :--- |
| `ACL_VLAN10_IN` | `Gig0/0.10` | `in` | VLAN 10 (LAB IoT) | 1. Deny lateral to VLAN 20, 30, 40.<br/>2. Permit TCP 8000/443 to `192.168.50.10`.<br/>3. Permit ICMP to Gateway/Server.<br/>4. Deny all other. |
| `ACL_VLAN20_IN` | `Gig0/0.20` | `in` | VLAN 20 (CLASS IoT) | 1. Deny lateral to VLAN 10, 30, 40.<br/>2. Permit TCP 8000/443 to `192.168.50.10`.<br/>3. Permit ICMP to Gateway/Server.<br/>4. Deny all other. |
| `ACL_VLAN30_IN` | `Gig0/0.30` | `in` | VLAN 30 (LIB/ADMIN IoT) | 1. Deny lateral to VLAN 10, 20, 40.<br/>2. Permit TCP 8000/443 to `192.168.50.10`.<br/>3. Permit ICMP to Gateway/Server.<br/>4. Deny all other. |
| `ACL_VLAN40_IN` | `Gig0/0.40` | `in` | VLAN 40 (USERS) | 1. Deny direct probe into IoT VLANs 10, 20, 30.<br/>2. Permit TCP 8000/443 to Backend (`.50.10`).<br/>3. Permit TCP 5173/80/443 to Dashboard (`.50.20`).<br/>4. Permit ICMP for diagnostics.<br/>5. Deny all other. |
