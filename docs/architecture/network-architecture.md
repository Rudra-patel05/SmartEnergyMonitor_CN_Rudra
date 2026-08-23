# Network Architecture

> Campus Network Design for Smart Energy Monitoring System

---

## 1. Overview

This document describes the **proposed campus network architecture** for the Smart Energy Monitoring System. The network is designed to connect IoT energy meters across four campus areas to a centralized backend server.

> **Note:** This is a **simulated network design** created for academic demonstration purposes using Cisco Packet Tracer. It does not represent an actual deployed campus network.

---

## 2. Network Topology

### Physical Topology

```
                        ┌──────────────┐
                        │   Internet    │
                        │   (Cloud)     │
                        └──────┬───────┘
                               │ Gi0/0
                        ┌──────▼───────┐
                        │  Core Router  │
                        │  (Router0)    │
                        │  Gateway      │
                        └──────┬───────┘
                               │ Gi0/1
                        ┌──────▼───────┐
                        │  Core Switch  │
                        │  (L3 Switch)  │
                        │  Inter-VLAN   │
                        └──┬───┬───┬──┬┘
                           │   │   │  │
              ┌────────────┘   │   │  └────────────┐
              │                │   │               │
       ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
       │ Access SW 1  │ │ Access SW 2  │ │ Access SW 3  │ │ Access SW 4  │
       │ (Computer    │ │ (Classroom)  │ │ (Library)    │ │ (Admin       │
       │    Lab)      │ │              │ │              │ │   Office)    │
       └──┬───┬──┬───┘ └──┬───┬──┬───┘ └──┬───┬──┬───┘ └──┬───┬──┬───┘
          │   │  │        │   │  │        │   │  │        │   │  │
          ▼   ▼  ▼        ▼   ▼  ▼        ▼   ▼  ▼        ▼   ▼  ▼
         IoT Devices    IoT Devices     IoT Devices     IoT Devices
         + PCs          + PCs           + PCs           + PCs
```

### Logical Topology
- **Star topology** within each campus area (devices connect to access switch)
- **Hierarchical design** with access, distribution, and core layers
- **Inter-VLAN routing** at the core switch/router level

---

## 3. Network Devices

| Device | Hostname | Model (Packet Tracer) | Role |
|--------|----------|----------------------|------|
| Core Router | Router0 | Cisco 2911 | Gateway, NAT, WAN connectivity |
| Core/Distribution Switch | CoreSwitch0 | Cisco 3560 (L3) | Inter-VLAN routing, traffic aggregation |
| Access Switch 1 | AccSW-Lab | Cisco 2960 | Computer Laboratory connectivity |
| Access Switch 2 | AccSW-Class | Cisco 2960 | Classroom connectivity |
| Access Switch 3 | AccSW-Lib | Cisco 2960 | Library connectivity |
| Access Switch 4 | AccSW-Admin | Cisco 2960 | Administrative Office connectivity |
| Backend Server | Server0 | Server-PT | FastAPI backend + database |
| IoT Meters | IoT-Lab-01, etc. | IoT Device / PC | Simulated energy meters |

---

## 4. VLAN Design

VLANs are used to segment network traffic by function and campus area for security and performance.

| VLAN ID | Name | Purpose | Subnet |
|---------|------|---------|--------|
| 10 | VLAN_IOT_LAB | IoT devices – Computer Lab | 192.168.10.0/24 |
| 20 | VLAN_IOT_CLASS | IoT devices – Classroom | 192.168.20.0/24 |
| 30 | VLAN_IOT_LIB | IoT devices – Library | 192.168.30.0/24 |
| 40 | VLAN_IOT_ADMIN | IoT devices – Admin Office | 192.168.40.0/24 |
| 50 | VLAN_SERVERS | Backend server and services | 192.168.50.0/24 |
| 60 | VLAN_MGMT | Network management | 192.168.60.0/24 |
| 99 | VLAN_NATIVE | Native VLAN (unused/security) | – |

---

## 5. IPv4 Addressing Scheme

### Subnet Allocation

| Network | Subnet | Gateway | Usable Range | Broadcast |
|---------|--------|---------|-------------|-----------|
| IoT – Lab | 192.168.10.0/24 | 192.168.10.1 | 192.168.10.2 – 192.168.10.254 | 192.168.10.255 |
| IoT – Classroom | 192.168.20.0/24 | 192.168.20.1 | 192.168.20.2 – 192.168.20.254 | 192.168.20.255 |
| IoT – Library | 192.168.30.0/24 | 192.168.30.1 | 192.168.30.2 – 192.168.30.254 | 192.168.30.255 |
| IoT – Admin | 192.168.40.0/24 | 192.168.40.1 | 192.168.40.2 – 192.168.40.254 | 192.168.40.255 |
| Servers | 192.168.50.0/24 | 192.168.50.1 | 192.168.50.2 – 192.168.50.254 | 192.168.50.255 |
| Management | 192.168.60.0/24 | 192.168.60.1 | 192.168.60.2 – 192.168.60.254 | 192.168.60.255 |

### Key Device IP Assignments

| Device | IP Address | VLAN | Notes |
|--------|-----------|------|-------|
| Core Router (Gi0/0) | DHCP / ISP assigned | – | WAN interface |
| Core Router (Gi0/1) | 192.168.50.1 | 50 | Server gateway |
| Core Switch (SVI VLAN 10) | 192.168.10.1 | 10 | Lab gateway |
| Core Switch (SVI VLAN 20) | 192.168.20.1 | 20 | Classroom gateway |
| Core Switch (SVI VLAN 30) | 192.168.30.1 | 30 | Library gateway |
| Core Switch (SVI VLAN 40) | 192.168.40.1 | 40 | Admin gateway |
| Core Switch (SVI VLAN 50) | 192.168.50.1 | 50 | Server gateway |
| Backend Server | 192.168.50.10 | 50 | Static IP |
| IoT Meter – Lab 01 | 192.168.10.101 | 10 | Static IP |
| IoT Meter – Class 01 | 192.168.20.101 | 20 | Static IP |
| IoT Meter – Lib 01 | 192.168.30.101 | 30 | Static IP |
| IoT Meter – Admin 01 | 192.168.40.101 | 40 | Static IP |

---

## 6. Inter-VLAN Routing

Inter-VLAN routing is handled by the **Core L3 Switch** using Switch Virtual Interfaces (SVIs).

### Configuration Concept

```
! Enable IP routing on L3 switch
ip routing

! Create SVIs for each VLAN
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
!
interface vlan 20
 ip address 192.168.20.1 255.255.255.0
 no shutdown
!
interface vlan 30
 ip address 192.168.30.1 255.255.255.0
 no shutdown
!
interface vlan 40
 ip address 192.168.40.1 255.255.255.0
 no shutdown
!
interface vlan 50
 ip address 192.168.50.1 255.255.255.0
 no shutdown
```

---

## 7. Access Control Lists (ACLs)

ACLs are used to enforce security policies at the network level.

### ACL Policy Summary

| Rule | Source | Destination | Action | Purpose |
|------|--------|-------------|--------|---------|
| 1 | IoT VLANs (10, 20, 30, 40) | Server VLAN (50) | **Permit** HTTP/HTTPS | Allow IoT data submission |
| 2 | IoT VLANs (10, 20, 30, 40) | IoT VLANs | **Deny** | Prevent IoT cross-VLAN talk |
| 3 | Management VLAN (60) | All VLANs | **Permit** | Allow network management |
| 4 | Any | Server VLAN (50) | **Deny** (except rule 1) | Protect server from unauthorized access |
| 5 | Server VLAN (50) | IoT VLANs | **Permit** | Allow server to query IoT devices |

### Example ACL Configuration

```
! ACL to allow IoT devices to reach server only on HTTP/HTTPS
access-list 100 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 443
access-list 100 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 80
access-list 100 deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
access-list 100 deny ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255
access-list 100 deny ip 192.168.10.0 0.0.0.255 192.168.40.0 0.0.0.255
access-list 100 permit ip 192.168.10.0 0.0.0.255 any

! Apply ACL to VLAN 10 SVI
interface vlan 10
 ip access-group 100 in
```

---

## 8. Trunk and Access Port Configuration

### Trunk Ports (Between Switches)

```
! Trunk port configuration (on access switch uplink)
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,60
 switchport trunk native vlan 99
```

### Access Ports (For End Devices)

```
! IoT device port in Computer Lab
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
```

---

## 9. Security Considerations

| Security Measure | Description |
|-----------------|-------------|
| **VLAN Segmentation** | Isolate IoT traffic from management and server traffic |
| **Native VLAN Hardening** | Set native VLAN to unused VLAN 99 to prevent VLAN hopping |
| **Port Security** | Limit MAC addresses per port to prevent unauthorized connections |
| **ACLs** | Restrict traffic flow between VLANs based on least-privilege |
| **SSH Management** | Use SSH (not Telnet) for switch/router management |
| **Disable Unused Ports** | Shutdown unused switch ports to prevent physical access attacks |
| **DHCP Snooping** | Prevent rogue DHCP servers (future enhancement) |

---

## 10. Network Diagram File

The complete network simulation will be saved as:
```
network/campus_network.pkt
```

This file can be opened in **Cisco Packet Tracer** for interactive simulation and testing.

---

*Document Version: 1.0 | Created: August 2026*
