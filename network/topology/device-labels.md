# 🏷️ Cisco Packet Tracer Device Label & Display Name Directory

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Network Architecture & Computer Networks (Day 11 & Day 12)  
> **Standard:** Cisco Packet Tracer 8.x+ Exact UI Labels

---

## 1. Network Infrastructure Devices

| Item # | PT Model / Icon | Workspace Display Label | CLI Hostname | Physical Location / Rack | Note / Primary Interface |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | **Router 2911** | `R1_CORE_ROUTER` | `R1_CORE_ROUTER` | Central Server Rack (L3 Core) | `Gig0/0` (Trunk to `SW_CORE_01`) |
| 2 | **Switch 2960-24TT** | `SW_CORE_01` | `SW_CORE_01` | Server Room (Distribution Layer) | `Gig0/1-3` (Trunks), `Fa0/1-4` (Servers) |
| 3 | **Switch 2960-24TT** | `SW_ACC_01` | `SW_ACC_01` | Academic Block A (Labs & Classes) | `Gig0/1` (Trunk), `Fa0/1-4` (IoT) |
| 4 | **Switch 2960-24TT** | `SW_ACC_02` | `SW_ACC_02` | Academic Block B (Admin & Users) | `Gig0/1` (Trunk), `Fa0/1-4` (IoT/PCs) |

---

## 2. Server Farm Devices

| Item # | PT Model / Icon | Workspace Display Label | CLI Hostname | IP Address | Connected Switch Port |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 5 | **Server-PT** | `SRV_BACKEND_01` | `SRV_BACKEND_01` | `192.168.50.10` | `SW_CORE_01: Fa0/1` (VLAN 50) |
| 6 | **Server-PT** | `SRV_FRONTEND_01` | `SRV_FRONTEND_01` | `192.168.50.20` | `SW_CORE_01: Fa0/2` (VLAN 50) |

---

## 3. IoT Energy Meter Nodes

| Item # | PT Model / Icon | Workspace Display Label | CLI Hostname | IP Address | Assigned VLAN | Connected Switch Port |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| 7 | **PC-PT / IoT** | `LAB-01` | `LAB-01` | `192.168.10.10` | 10 | `SW_ACC_01: Fa0/1` |
| 8 | **PC-PT / IoT** | `LAB-02` | `LAB-02` | `192.168.10.11` | 10 | `SW_ACC_01: Fa0/2` |
| 9 | **PC-PT / IoT** | `CLASS-01` | `CLASS-01` | `192.168.20.10` | 20 | `SW_ACC_01: Fa0/3` |
| 10 | **PC-PT / IoT** | `CLASS-02` | `CLASS-02` | `192.168.20.11` | 20 | `SW_ACC_01: Fa0/4` |
| 11 | **PC-PT / IoT** | `LIB-01` | `LIB-01` | `192.168.30.10` | 30 | `SW_ACC_02: Fa0/1` |
| 12 | **PC-PT / IoT** | `ADMIN-01` | `ADMIN-01` | `192.168.30.20` | 30 | `SW_ACC_02: Fa0/2` |

---

## 4. User Workstations & Operator Terminals

| Item # | PT Model / Icon | Workspace Display Label | CLI Hostname | IP Address | Assigned VLAN | Connected Switch Port |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| 13 | **PC-PT** | `PC_FACULTY_01` | `PC_FACULTY_01` | `192.168.40.10` | 40 | `SW_ACC_02: Fa0/3` |
| 14 | **Laptop-PT** | `PC_STUDENT_01` | `PC_STUDENT_01` | `192.168.40.11` | 40 | `SW_ACC_02: Fa0/4` |

---

## 5. Visual Placement Layout Grid

```
+---------------------------------------------------------------------------------------+
|                                    CISCO PACKET TRACER                                |
|                                                                                       |
|                                    [ R1_CORE_ROUTER ]                                 |
|                                            | (Gig0/0)                                 |
|                                            | (Gig0/1)                                 |
|                                      [ SW_CORE_01 ]                                   |
|                          (Gig0/2)  /                \  (Gig0/3)                       |
|                       ┌───────────┘                  └───────────┐                    |
|                       │ (Gig0/1)                                 │ (Gig0/1)           |
|                 [ SW_ACC_01 ]                              [ SW_ACC_02 ]              |
|              ┌───┬───┬───┬───┐                          ┌───┬───┬───┬───┐             |
|             Fa1 Fa2 Fa3 Fa4                            Fa1 Fa2 Fa3 Fa4                |
|              │   │   │   │                              │   │   │   │                 |
|             [L1][L2][C1][C2]                           [LB][AD][PF][PS]               |
|                                                                                       |
|  Server Farm (Connected to SW_CORE_01):                                               |
|    Fa0/1: [ SRV_BACKEND_01 ] (192.168.50.10)                                          |
|    Fa0/2: [ SRV_FRONTEND_01 ] (192.168.50.20)                                         |
+---------------------------------------------------------------------------------------+
```
