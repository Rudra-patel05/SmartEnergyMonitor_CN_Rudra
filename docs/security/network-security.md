# 🕸️ Network Security & Segmentation Architecture

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Network Architecture & Computer Networks (Day 11 & Day 12)  
> **Institution:** Gujarat Technological University – Computer Engineering

---

## 1. Network Subnet Segmentation

The Smart Campus network isolates virtual elements into Layer-2 domains using **IEEE 802.1Q VLANs**. Inter-VLAN traffic routing is managed by the Core Router (R1) using **Router-on-a-Stick (ROAS)**.

```
       [ VLAN 10 (LAB IoT) ]        ───┐
                                       ├───> [ Core Router (R1) ]
       [ VLAN 20 (CLASS IoT) ]      ───┤           │
                                       │           v [Extended ACL Filters]
       [ VLAN 30 (ADMIN IoT) ]      ───┤           │
                                       ├───> [ VLAN 50 (Server Farm) ]
       [ VLAN 40 (Users/Staff) ]    ───┘
```

---

## 2. Cisco Access Control Lists (ACLs) Configuration

Security rules are enforced directly on R1's sub-interfaces via Extended Access Control Lists.

### 2.1. Ingestion Isolation (VLAN 10, 20, 30 ACL)
These ACL rules permit outbound REST API transmission to the server subnet while blocking lateral movement:
```cisco
! Permitted: Ingestion requests to backend API server on port 8000
permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 8000
! Permitted: ICMP for networking diagnostics
permit icmp 192.168.10.0 0.0.0.255 any
! Denied: Direct access to other campus VLANs (isolation)
deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255 log
deny ip 192.168.10.0 0.0.0.255 192.168.40.0 0.0.0.255 log
! Denied: All other traffic
deny ip any any log
```

### 2.2. User Dashboard Isolation (VLAN 40 ACL)
This ACL allows administrators and campus operators to access the React dashboard and API while preventing them from connecting directly to the IoT energy meters:
```cisco
! Permitted: Access Web Dashboard (port 5173, 80) and API (port 8000)
permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.20 eq 5173
permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.10 eq 8000
! Denied: Accessing IoT microcontrollers directly
deny ip 192.168.40.0 0.0.0.255 192.168.10.0 0.0.0.255 log
deny ip 192.168.40.0 0.0.0.255 192.168.20.0 0.0.0.255 log
```

---

## 3. Switch Port Hardening Specifications

Access switches (`SW-ACC-01`, `SW-ACC-02`) enforce the following security protocols:
1. **Unused Port Shutdown:** All unused switch interfaces (e.g. `Fa0/5` to `Fa0/24` on `SW-ACC-01`) are administratively disabled (`shutdown`) in config scripts to prevent unauthorized local plug-in attacks.
2. **Native VLAN Tagging:** The default VLAN 1 is disabled. Management SVIs and Native Trunk untagged traffic are redirected to VLAN 99 to mitigate VLAN hopping attacks.
3. **Loop Mitigation:** Spanning Tree PortFast is configured on all edge ports connecting to endpoints to speed up convergence while preventing loop formation.
