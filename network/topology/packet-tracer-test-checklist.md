# 📋 Cisco Packet Tracer Verification & Test Checklist

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Network Architecture & Computer Networks (Day 11 & Day 12)  
> **Target Topology:** `smart_campus_network.pkt`  
> **Auditor / Tester:** Manual Entry Lab Sheet

---

## 1. Connectivity & ACL Security Test Cases

| Test # | Source Device | Destination / Target | Command Executed | Expected Result (Derived from Final ACL) | Actual Result (Manual Entry) | Status (PASS / FAIL) |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | `LAB-01` (`192.168.10.10`) | Default Gateway (`192.168.10.1`) | `ping 192.168.10.1` | **SUCCESS** (4/4 packets received, TTL=255, <1ms) | `[ ] Pending Manual Test` | `[ ]` |
| **TC-02** | `LAB-01` (`192.168.10.10`) | Backend Server (`192.168.50.10`) | `ping 192.168.50.10` | **SUCCESS** (Permitted by `ACL_VLAN10_IN` ICMP rule to Server subnet) | `[ ] Pending Manual Test` | `[ ]` |
| **TC-03** | `PC_FACULTY_01` (`192.168.40.10`) | Backend Server (`192.168.50.10`) | `ping 192.168.50.10` | **SUCCESS** (Permitted by `ACL_VLAN40_IN` ICMP rule to Server subnet) | `[ ] Pending Manual Test` | `[ ]` |
| **TC-04** | `LAB-01` (`192.168.10.10`) | `CLASS-01` (`192.168.20.10`) | `ping 192.168.20.10` | **BLOCKED** (`Request timed out.` Dropped by `ACL_VLAN10_IN` lateral deny rule) | `[ ] Pending Manual Test` | `[ ]` |
| **TC-05** | `LAB-01` (`192.168.10.10`) | `LIB-01` (`192.168.30.10`) | `ping 192.168.30.10` | **BLOCKED** (`Request timed out.` Dropped by `ACL_VLAN10_IN` lateral deny rule) | `[ ] Pending Manual Test` | `[ ]` |
| **TC-06** | `LAB-01` (`192.168.10.10`) | `PC_FACULTY_01` (`192.168.40.10`) | `ping 192.168.40.10` | **BLOCKED** (`Request timed out.` Dropped by `ACL_VLAN10_IN` user isolation rule) | `[ ] Pending Manual Test` | `[ ]` |
| **TC-07** | `PC_FACULTY_01` (`192.168.40.10`) | `LAB-01` (`192.168.10.10`) | `ping 192.168.10.10` | **BLOCKED** (`Request timed out.` Dropped by `ACL_VLAN40_IN` anti-tamper rule) | `[ ] Pending Manual Test` | `[ ]` |
| **TC-08** | `PC_FACULTY_01` (`192.168.40.10`) | Frontend Server (`192.168.50.20`) | `ping 192.168.50.20` | **SUCCESS** (Permitted by `ACL_VLAN40_IN` rule) | `[ ] Pending Manual Test` | `[ ]` |
| **TC-09** | `CLASS-01` (`192.168.20.10`) | Default Gateway (`192.168.20.1`) | `ping 192.168.20.1</a>` | **SUCCESS** (4/4 packets received, TTL=255) | `[ ] Pending Manual Test` | `[ ]` |
| **TC-10** | `LIB-01` (`192.168.30.10`) | Backend Server (`192.168.50.10`) | `ping 192.168.50.10` | **SUCCESS** (Permitted by `ACL_VLAN30_IN`) | `[ ] Pending Manual Test` | `[ ]` |

---

## 2. Cisco IOS Command & Infrastructure Verification Table

| Test # | Target Device | Verification Focus | Command | Expected Output Criteria | Actual Result (Manual Entry) | Status |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **IV-01** | `SW_CORE_01` | VLAN Database | `show vlan brief` | VLANs `10, 20, 30, 40, 50, 99` exist and are active. `Fa0/1-4` in VLAN 50. | `[ ] Pending Manual Run` | `[ ]` |
| **IV-02** | `SW_ACC_01` | VLAN Database | `show vlan brief` | VLANs `10, 20, 99` active. `Fa0/1-2` in VLAN 10, `Fa0/3-4` in VLAN 20. | `[ ] Pending Manual Run` | `[ ]` |
| **IV-03** | `SW_ACC_02` | VLAN Database | `show vlan brief` | VLANs `30, 40, 99` active. `Fa0/1-2` in VLAN 30, `Fa0/3-12` in VLAN 40. | `[ ] Pending Manual Run` | `[ ]` |
| **IV-04** | `SW_CORE_01` | 802.1Q Trunks | `show interfaces trunk` | `Gig0/1`, `Gig0/2`, `Gig0/3` trunking, 802.1q, Native VLAN 99. | `[ ] Pending Manual Run` | `[ ]` |
| **IV-05** | `SW_ACC_01` | 802.1Q Trunk | `show interfaces trunk` | `Gig0/1` trunking, Native VLAN 99, Allowed VLANs `10, 20, 99`. | `[ ] Pending Manual Run` | `[ ]` |
| **IV-06** | `SW_ACC_02` | 802.1Q Trunk | `show interfaces trunk` | `Gig0/1` trunking, Native VLAN 99, Allowed VLANs `30, 40, 99`. | `[ ] Pending Manual Run` | `[ ]` |
| **IV-07** | `R1_CORE_ROUTER`| Subinterface Status | `show ip interface brief` | `Gig0/0` is up/up. Subinterfaces `.10, .20, .30, .40, .50, .99` all up/up. | `[ ] Pending Manual Run` | `[ ]` |
| **IV-08** | `R1_CORE_ROUTER`| Routing Table | `show ip route` | 6 connected routes (`192.168.10.0/24` through `192.168.99.0/24`) present as `C`. | `[ ] Pending Manual Run` | `[ ]` |
| **IV-09** | `R1_CORE_ROUTER`| Subinterface Encapsulation | `show running-config interface GigabitEthernet0/0.10` | Shows `encapsulation dot1Q 10` and `ip access-group ACL_VLAN10_IN in`. | `[ ] Pending Manual Run` | `[ ]` |
| **IV-10** | `R1_CORE_ROUTER`| Access Control Lists | `show access-lists` | Extended ACLs `ACL_VLAN10_IN`, `ACL_VLAN20_IN`, `ACL_VLAN30_IN`, `ACL_VLAN40_IN` listed with match counters. | `[ ] Pending Manual Run` | `[ ]` |

---

## 3. Manual Sign-Off Sheet

```
Tester Name: _______________________
Date Tested: _______________________
Packet Tracer Version: ______________
Topology File: smart_campus_network.pkt
Overall Result: [ ] PASS   [ ] FAIL
Comments: __________________________________________________________________
```
