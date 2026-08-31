# 🔀 Inter-VLAN Routing & Router-on-a-Stick (ROAS) Design

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Network Architecture & Computer Networks (Day 11)  
> **Institution:** Gujarat Technological University – Computer Engineering

---

## 1. Inter-VLAN Routing Concept

Because each VLAN represents an independent Layer-2 broadcast domain, packets cannot traverse between different VLANs (e.g. from IoT Meter `192.168.10.10` in VLAN 10 to Backend Server `192.168.50.10` in VLAN 50) without a Layer-3 routing device.

In this architecture, **Router-on-a-Stick (ROAS)** is implemented on the Core Router (`R1` — Cisco 2911 / 4321 series) over a single physical GigabitEthernet link (`Gig0/0`).

```
                    ┌─────────────────────────┐
                    │    Core Router (R1)     │
                    │   Gig0/0 (Trunk Link)   │
                    └────────────┬────────────┘
                                 │
           ┌─────────────────────┴─────────────────────┐
           │ 802.1Q Multiplexed Trunk (Sub-Interfaces) │
           │  • Gig0/0.10 -> VLAN 10 (192.168.10.1/24) │
           │  • Gig0/0.20 -> VLAN 20 (192.168.20.1/24) │
           │  • Gig0/0.30 -> VLAN 30 (192.168.30.1/24) │
           │  • Gig0/0.40 -> VLAN 40 (192.168.40.1/24) │
           │  • Gig0/0.50 -> VLAN 50 (192.168.50.1/24) │
           │  • Gig0/0.99 -> VLAN 99 (192.168.99.1/24) │
           └─────────────────────┬─────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │  Core Switch (SW-CORE)  │
                    └────────────┬────────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
     ┌──────┴──────┐      ┌──────┴──────┐      ┌──────┴──────┐
     │  SW-ACC-01  │      │  SW-ACC-02  │      │ Server Farm │
     │  (VLAN 10,  │      │  (VLAN 30,  │      │  (VLAN 50)  │
     │   VLAN 20)  │      │   VLAN 40)  │      │             │
     └─────────────┘      └─────────────┘      └─────────────┘
```

---

## 2. Cisco IOS Sub-Interface Specification

The physical interface `GigabitEthernet0/0` on Router `R1` is enabled without an IP address. Logical sub-interfaces are created, each bound to an IEEE 802.1Q tag corresponding to its respective VLAN:

```cisco
interface GigabitEthernet0/0
 no ip address
 no shutdown
!
interface GigabitEthernet0/0.10
 description Gateway for LAB IoT (VLAN 10)
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
!
interface GigabitEthernet0/0.20
 description Gateway for CLASSROOM IoT (VLAN 20)
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
!
interface GigabitEthernet0/0.30
 description Gateway for LIB/ADMIN IoT (VLAN 30)
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
!
interface GigabitEthernet0/0.40
 description Gateway for USERS/DASHBOARD (VLAN 40)
 encapsulation dot1Q 40
 ip address 192.168.40.1 255.255.255.0
!
interface GigabitEthernet0/0.50
 description Gateway for SERVERS/BACKEND (VLAN 50)
 encapsulation dot1Q 50
 ip address 192.168.50.1 255.255.255.0
!
interface GigabitEthernet0/0.99
 description Gateway for MANAGEMENT (VLAN 99)
 encapsulation dot1Q 99 native
 ip address 192.168.99.1 255.255.255.0
```

---

## 3. End-to-End Packet Routing Walkthrough

### Scenario: IoT Meter `LAB-01` (`192.168.10.10`) POSTs Telemetry to Backend Server (`192.168.50.10`)

1. **Layer 3 Evaluation:**
   - Host `LAB-01` calculates destination network: `192.168.50.10 & 255.255.255.0 = 192.168.50.0`.
   - Since destination is on a remote subnet, packet is sent to Default Gateway (`192.168.10.1`).
2. **Layer 2 Encapsulation & Tagging:**
   - Host sends untagged Ethernet frame to Access Switch `SW-ACC-01` port `Fa0/1`.
   - `SW-ACC-01` inserts 802.1Q header with `VLAN ID = 10` and forwards via trunk port `Gig0/1`.
   - `SW-CORE-01` receives tagged frame and forwards it over trunk `Gig0/1` to Router `R1`.
3. **Layer 3 Routing & De-encapsulation:**
   - Router `R1` receives frame on sub-interface `Gig0/0.10` (matching VLAN tag 10).
   - R1 strips 802.1Q header, inspects IP destination `192.168.50.10`, and consults routing table.
   - R1 matches route `192.168.50.0/24` directly connected via sub-interface `Gig0/0.50`.
   - R1 checks Inbound/Outbound Access Control Lists (ACLs) to ensure HTTP/REST traffic is permitted.
4. **Outbound Tagging & Delivery:**
   - R1 encapsulates IP packet in new Ethernet frame with 802.1Q `VLAN ID = 50` and transmits out `Gig0/0.50`.
   - `SW-CORE-01` inspects MAC address table for VLAN 50, removes VLAN tag, and delivers frame to Backend Server port `Fa0/1`.
