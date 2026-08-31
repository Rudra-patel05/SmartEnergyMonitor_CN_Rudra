# 💻 Cisco IOS Configuration Scripts (Copy-Paste Ready)

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Network Architecture & Computer Networks (Day 11)  
> **Device Targets:** Cisco 2911 / 4321 Router, Cisco Catalyst 2960 / 3560 Switches

---

## 1. Router R1 (Core Router / Default Gateway)

```cisco
! =========================================================================
! ROUTER R1 — INTER-VLAN ROUTER-ON-A-STICK CONFIGURATION
! =========================================================================
enable
configure terminal
hostname R1_CORE_ROUTER

! Disable DNS lookup for typos
no ip domain-lookup

! Enable physical trunk port
interface GigabitEthernet0/0
 description Trunk Link to SW_CORE_01
 no ip address
 duplex auto
 speed auto
 no shutdown
exit

! Sub-Interface for VLAN 10 (LAB IoT)
interface GigabitEthernet0/0.10
 description Gateway for LAB IoT (VLAN 10)
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit

! Sub-Interface for VLAN 20 (CLASSROOM IoT)
interface GigabitEthernet0/0.20
 description Gateway for CLASSROOM IoT (VLAN 20)
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
 no shutdown
exit

! Sub-Interface for VLAN 30 (LIB/ADMIN IoT)
interface GigabitEthernet0/0.30
 description Gateway for LIB/ADMIN IoT (VLAN 30)
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
 no shutdown
exit

! Sub-Interface for VLAN 40 (USERS)
interface GigabitEthernet0/0.40
 description Gateway for USERS (VLAN 40)
 encapsulation dot1Q 40
 ip address 192.168.40.1 255.255.255.0
 no shutdown
exit

! Sub-Interface for VLAN 50 (SERVERS & BACKEND)
interface GigabitEthernet0/0.50
 description Gateway for SERVERS & BACKEND (VLAN 50)
 encapsulation dot1Q 50
 ip address 192.168.50.1 255.255.255.0
 no shutdown
exit

! Sub-Interface for VLAN 99 (MANAGEMENT NATIVE)
interface GigabitEthernet0/0.99
 description Gateway for MANAGEMENT (VLAN 99)
 encapsulation dot1Q 99 native
 ip address 192.168.99.1 255.255.255.0
 no shutdown
exit

! -------------------------------------------------------------------------
! ACCESS CONTROL LISTS (SECURITY SEGMENTATION)
! -------------------------------------------------------------------------
ip access-list extended ACL_VLAN10_IN
 permit icmp 192.168.10.0 0.0.0.255 any
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 8000
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 443
 deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255 log
 deny ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255 log
 deny ip 192.168.10.0 0.0.0.255 192.168.40.0 0.0.0.255 log
 deny ip any any log
exit

ip access-list extended ACL_VLAN20_IN
 permit icmp 192.168.20.0 0.0.0.255 any
 permit tcp 192.168.20.0 0.0.0.255 host 192.168.50.10 eq 8000
 permit tcp 192.168.20.0 0.0.0.255 host 192.168.50.10 eq 443
 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255 log
 deny ip 192.168.20.0 0.0.0.255 192.168.30.0 0.0.0.255 log
 deny ip 192.168.20.0 0.0.0.255 192.168.40.0 0.0.0.255 log
 deny ip any any log
exit

ip access-list extended ACL_VLAN40_IN
 permit icmp 192.168.40.0 0.0.0.255 any
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.10 eq 8000
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.10 eq 443
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.20 eq 5173
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.20 eq 80
 deny ip 192.168.40.0 0.0.0.255 192.168.10.0 0.0.0.255 log
 deny ip 192.168.40.0 0.0.0.255 192.168.20.0 0.0.0.255 log
 deny ip 192.168.40.0 0.0.0.255 192.168.30.0 0.0.0.255 log
 deny ip any any log
exit

! Apply ACLs to Sub-Interfaces
interface GigabitEthernet0/0.10
 ip access-group ACL_VLAN10_IN in
exit

interface GigabitEthernet0/0.20
 ip access-group ACL_VLAN20_IN in
exit

interface GigabitEthernet0/0.40
 ip access-group ACL_VLAN40_IN in
exit

! Save configuration
end
write memory
```

---

## 2. Core Switch (`SW-CORE-01`)

```cisco
! =========================================================================
! CORE SWITCH SW-CORE-01 CONFIGURATION
! =========================================================================
enable
configure terminal
hostname SW_CORE_01

! Create VLAN Database
vlan 10
 name VLAN_LAB_IOT
vlan 20
 name VLAN_CLASS_IOT
vlan 30
 name VLAN_LIB_ADMIN_IOT
vlan 40
 name VLAN_USERS
vlan 50
 name VLAN_SERVERS
vlan 99
 name VLAN_MANAGEMENT
exit

! Trunk to Router R1
interface GigabitEthernet0/1
 description Trunk to Router R1 Gig0/0
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
exit

! Trunk to Access Switch 1 (Labs & Classrooms)
interface GigabitEthernet0/2
 description Trunk to SW_ACC_01 Gig0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,99
 no shutdown
exit

! Trunk to Access Switch 2 (Library, Admin & Users)
interface GigabitEthernet0/3
 description Trunk to SW_ACC_02 Gig0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 30,40,99
 no shutdown
exit

! Access Ports for Server Farm (VLAN 50)
interface range FastEthernet0/1 - 4
 description Server Farm Access Ports (FastAPI & Dashboard)
 switchport mode access
 switchport access vlan 50
 spanning-tree portfast
 no shutdown
exit

! SVI Management Interface
interface vlan 99
 ip address 192.168.99.2 255.255.255.0
 no shutdown
exit

ip default-gateway 192.168.99.1

end
write memory
```

---

## 3. Access Switch 1 (`SW-ACC-01` — Labs & Classrooms)

```cisco
! =========================================================================
! ACCESS SWITCH 1 CONFIGURATION
! =========================================================================
enable
configure terminal
hostname SW_ACC_01

vlan 10
 name VLAN_LAB_IOT
vlan 20
 name VLAN_CLASS_IOT
vlan 99
 name VLAN_MANAGEMENT
exit

! Trunk Uplink to Core Switch
interface GigabitEthernet0/1
 description Uplink to SW_CORE_01 Gig0/2
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,99
 no shutdown
exit

! Lab IoT Meter Ports (VLAN 10)
interface range FastEthernet0/1 - 2
 description Computer Lab IoT Meters (LAB-01, LAB-02)
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
exit

! Classroom IoT Meter Ports (VLAN 20)
interface range FastEthernet0/3 - 4
 description Classroom IoT Meters (CLASS-01, CLASS-02)
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 no shutdown
exit

! Security Hardening: Disable unused ports
interface range FastEthernet0/5 - 24, GigabitEthernet0/2
 shutdown
exit

! SVI Management Interface
interface vlan 99
 ip address 192.168.99.11 255.255.255.0
 no shutdown
exit

ip default-gateway 192.168.99.1

end
write memory
```

---

## 4. Access Switch 2 (`SW-ACC-02` — Library, Admin & Users)

```cisco
! =========================================================================
! ACCESS SWITCH 2 CONFIGURATION
! =========================================================================
enable
configure terminal
hostname SW_ACC_02

vlan 30
 name VLAN_LIB_ADMIN_IOT
vlan 40
 name VLAN_USERS
vlan 99
 name VLAN_MANAGEMENT
exit

! Trunk Uplink to Core Switch
interface GigabitEthernet0/1
 description Uplink to SW_CORE_01 Gig0/3
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 30,40,99
 no shutdown
exit

! Library & Admin IoT Meter Ports (VLAN 30)
interface range FastEthernet0/1 - 2
 description Library & Admin IoT Meters (LIB-01, ADMIN-01)
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 no shutdown
exit

! User & Workstation Access Ports (VLAN 40)
interface range FastEthernet0/3 - 12
 description User Workstations & Dashboard Clients
 switchport mode access
 switchport access vlan 40
 spanning-tree portfast
 no shutdown
exit

! Security Hardening: Disable unused ports
interface range FastEthernet0/13 - 24, GigabitEthernet0/2
 shutdown
exit

! SVI Management Interface
interface vlan 99
 ip address 192.168.99.12 255.255.255.0
 no shutdown
exit

ip default-gateway 192.168.99.1

end
write memory
```
