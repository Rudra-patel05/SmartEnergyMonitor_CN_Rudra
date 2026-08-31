# 🛡️ Network Security Rules & Cisco Access Control Lists (ACLs)

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Network Architecture & Computer Networks (Day 11 & Day 12)  
> **Institution:** Gujarat Technological University – Computer Engineering

---

## 1. Network Security Objective & Zero-Trust Matrix

The network follows the principle of least privilege and strict micro-segmentation:
- **Rule 1 (IoT Ingestion):** IoT Meters (VLANs 10, 20, 30) can **ONLY** communicate with the FastAPI Backend Server (`192.168.50.10`) on TCP port `8000` (and `443` for TLS).
- **Rule 2 (Lateral IoT Isolation):** IoT devices are strictly forbidden from communicating with other IoT devices across VLANs or within their own subnet.
- **Rule 3 (IoT to User Isolation):** IoT devices are prohibited from initiating any connection to User/Faculty workstations (VLAN 40).
- **Rule 4 (User Dashboard Access):** User workstations (VLAN 40) are permitted to access the Web Dashboard (port 5173 / 80 / 443) and FastAPI REST endpoints (port 8000). Direct SSH/DB access to server infrastructure is restricted.
- **Rule 5 (Default Deny):** All other cross-VLAN packets are dropped and logged by an explicit `deny ip any any log` rule.

---

## 2. Traffic Flow & ACL Matrix

| Source Subnet | Destination Subnet | Protocol / Port | Action | Purpose / Rationale |
| :--- | :--- | :--- | :---: | :--- |
| **VLAN 10, 20, 30 (IoT)** | `192.168.50.10` (Backend) | `TCP 8000, 443` | **PERMIT** | Telemetry ingestion (`POST /api/energy/readings`) |
| **VLAN 10, 20, 30 (IoT)** | `192.168.10.0-30.0` (IoT) | `ALL` | **DENY** | Block lateral pivoting between compromised meters |
| **VLAN 10, 20, 30 (IoT)** | `192.168.40.0/24` (Users) | `ALL` | **DENY** | Protect user laptops from rogue IoT scanning |
| **VLAN 40 (Users)** | `192.168.50.10` (Backend) | `TCP 8000, 443` | **PERMIT** | API calls, AI inference, and summary queries |
| **VLAN 40 (Users)** | `192.168.50.20` (Frontend) | `TCP 5173, 80, 443` | **PERMIT** | Web dashboard browser GUI access |
| **VLAN 40 (Users)** | `192.168.10.0-30.0` (IoT) | `ALL` | **DENY** | Prevent unauthorized tampering with IoT meters |
| **Any Subnet** | **Any Subnet** | `ICMP (Ping)` | **PERMIT (Internal)** | Network diagnostic & latency monitoring |
| **Any Other Traffic** | **Any Other Destination** | `ALL` | **DENY** | Strict implicit deny baseline |

---

## 3. Cisco IOS Extended ACL Implementation

Applied inbound on Router `R1` sub-interfaces:

```cisco
! =========================================================================
! ACL 110: LAB IoT Security Filter (Applied Inbound on Gig0/0.10)
! =========================================================================
ip access-list extended ACL_VLAN10_IN
 remark Allow ICMP Echo/Reply for ping testing
 permit icmp 192.168.10.0 0.0.0.255 any
 remark Allow REST HTTP Telemetry to Backend Server ONLY
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 8000
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 443
 remark Explicit Deny for all other lateral & user traffic
 deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255 log
 deny ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255 log
 deny ip 192.168.10.0 0.0.0.255 192.168.40.0 0.0.0.255 log
 deny ip any any log
!
interface GigabitEthernet0/0.10
 ip access-group ACL_VLAN10_IN in
!

! =========================================================================
! ACL 120: CLASSROOM IoT Security Filter (Applied Inbound on Gig0/0.20)
! =========================================================================
ip access-list extended ACL_VLAN20_IN
 permit icmp 192.168.20.0 0.0.0.255 any
 permit tcp 192.168.20.0 0.0.0.255 host 192.168.50.10 eq 8000
 permit tcp 192.168.20.0 0.0.0.255 host 192.168.50.10 eq 443
 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255 log
 deny ip 192.168.20.0 0.0.0.255 192.168.30.0 0.0.0.255 log
 deny ip 192.168.20.0 0.0.0.255 192.168.40.0 0.0.0.255 log
 deny ip any any log
!
interface GigabitEthernet0/0.20
 ip access-group ACL_VLAN20_IN in
!

! =========================================================================
! ACL 140: USERS Security Filter (Applied Inbound on Gig0/0.40)
! =========================================================================
ip access-list extended ACL_VLAN40_IN
 permit icmp 192.168.40.0 0.0.0.255 any
 remark Allow Web Dashboard & API Server Access
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.10 eq 8000
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.10 eq 443
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.20 eq 5173
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.20 eq 80
 remark Block direct user connection into raw IoT hardware meters
 deny ip 192.168.40.0 0.0.0.255 192.168.10.0 0.0.0.255 log
 deny ip 192.168.40.0 0.0.0.255 192.168.20.0 0.0.0.255 log
 deny ip 192.168.40.0 0.0.0.255 192.168.30.0 0.0.0.255 log
 deny ip any any log
!
interface GigabitEthernet0/0.40
 ip access-group ACL_VLAN40_IN in
```
