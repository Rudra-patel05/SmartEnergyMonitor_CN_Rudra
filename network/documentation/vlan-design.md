# 🏷️ VLAN Architecture & Switch Port Allocation Plan

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Network Architecture & Computer Networks (Day 11)  
> **Institution:** Gujarat Technological University – Computer Engineering

---

## 1. VLAN Design Rationale & Principles

In a modern smart-campus environment, connecting hundreds of headless IoT sensors, student laptops, faculty computers, and central database servers to a single flat Layer-2 network creates severe vulnerabilities:
1. **Broadcast Storm Vulnerability:** Unrestricted Layer-2 broadcasts (ARP, DHCP discoveries) consume sensor MCU cycles and network bandwidth.
2. **Eavesdropping & MITM Risks:** Unsegmented networks allow unauthorized users to capture plaintext telemetry or inject spoofed data.
3. **Lateral Attack Propagation:** A compromised IoT microcontroller could be used as a stepping stone to pivot into academic database servers or administrative workstations.

To eliminate these risks, **IEEE 802.1Q Virtual Local Area Networks (VLANs)** logically isolate traffic at the Data Link Layer (Layer 2).

---

## 2. Campus VLAN Segmentation Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SMART CAMPUS VLAN MATRIX                        │
├─────────┬────────────────────┬────────────────────┬────────────────────┤
│ VLAN ID │ VLAN Name          │ Broadcast Domain   │ Security Tier      │
├─────────┼────────────────────┼────────────────────┼────────────────────┤
│ VLAN 10 │ VLAN_LAB_IOT       │ 192.168.10.0/24    │ Tier 3 (Restricted)│
│ VLAN 20 │ VLAN_CLASS_IOT     │ 192.168.20.0/24    │ Tier 3 (Restricted)│
│ VLAN 30 │ VLAN_LIB_ADMIN_IOT │ 192.168.30.0/24    │ Tier 3 (Restricted)│
│ VLAN 40 │ VLAN_USERS         │ 192.168.40.0/24    │ Tier 2 (Standard)  │
│ VLAN 50 │ VLAN_SERVERS       │ 192.168.50.0/24    │ Tier 1 (High Sec)  │
│ VLAN 99 │ VLAN_MANAGEMENT    │ 192.168.99.0/24    │ Tier 0 (Isolated)  │
└─────────┴────────────────────┴────────────────────┴────────────────────┘
```

---

## 3. Switch Port Allocation & Interface Mapping

### 3.1. Core Switch (`SW-CORE-01` — Cisco Catalyst 2960 / 3560)

| Interface | Link Type | Connected Device / Endpoint | Native / Allowed VLANs |
| :--- | :--- | :--- | :--- |
| `Gig0/1` | **802.1Q Trunk** | Router `R1` (`Gig0/0`) | Allowed: 10, 20, 30, 40, 50, 99 (Native: 99) |
| `Gig0/2` | **802.1Q Trunk** | Access Switch `SW-ACC-01` (`Gig0/1`) | Allowed: 10, 20, 99 (Native: 99) |
| `Gig0/3` | **802.1Q Trunk** | Access Switch `SW-ACC-02` (`Gig0/1`) | Allowed: 30, 40, 99 (Native: 99) |
| `Fa0/1` – `Fa0/4` | **Access (VLAN 50)** | Server Farm (FastAPI Backend, DB) | Access: VLAN 50 |
| `Fa0/24` | **Access (VLAN 99)** | Network Admin Console (OOB Management)| Access: VLAN 99 |

### 3.2. Access Switch 1 (`SW-ACC-01` — Labs & Classrooms)

| Interface | Mode | Assigned VLAN | Connected Endpoint |
| :--- | :--- | :---: | :--- |
| `Gig0/1` | **802.1Q Trunk** | 10, 20, 99 | Uplink to `SW-CORE-01` (`Gig0/2`) |
| `Fa0/1` – `Fa0/2` | Access | **VLAN 10** | Computer Lab 1 & 2 Energy Meters (`LAB-01`, `LAB-02`) |
| `Fa0/3` – `Fa0/4` | Access | **VLAN 20** | Classroom 101 & 102 Energy Meters (`CLASS-01`, `CLASS-02`) |
| `Fa0/5` – `Fa0/24`| Access (Disabled)| Unused | Shut down (`shutdown`) for security hardening |

### 3.3. Access Switch 2 (`SW-ACC-02` — Library, Admin & Users)

| Interface | Mode | Assigned VLAN | Connected Endpoint |
| :--- | :--- | :---: | :--- |
| `Gig0/1` | **802.1Q Trunk** | 30, 40, 99 | Uplink to `SW-CORE-01` (`Gig0/3`) |
| `Fa0/1` | Access | **VLAN 30** | Central Library Energy Meter (`LIB-01`) |
| `Fa0/2` | Access | **VLAN 30** | Administrative Building Energy Meter (`ADMIN-01`) |
| `Fa0/3` – `Fa0/12`| Access | **VLAN 40** | Student/Faculty Workstations & Dashboard Clients |
| `Fa0/13` – `Fa0/24`| Access (Disabled)| Unused | Shut down (`shutdown`) for security hardening |

---

## 4. 802.1Q Trunking Protocol & Tagging

- **Encapsulation:** IEEE 802.1Q header insertion (4-byte tag including 12-bit VLAN ID).
- **Native VLAN:** VLAN 99 is assigned as the untagged Native VLAN across all trunk links to mitigate VLAN Hopping / Double Tagging attacks. Default VLAN 1 is explicitly disabled on all inter-switch trunks.
