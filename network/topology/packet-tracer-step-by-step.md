# 🛠️ Cisco Packet Tracer Step-by-Step Implementation Procedure

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Network Architecture & Computer Networks (Day 11 & Day 12)  
> **Target Simulator:** Cisco Packet Tracer 8.x+  
> **Format:** Beginner-Friendly Guided Lab Procedure

---

## Overview

Follow this step-by-step guide to build, cable, configure, and verify the Smart Campus Network topology in Cisco Packet Tracer.

---

## PHASE A: Place Devices in Workspace

Open Cisco Packet Tracer and drag the following **14 devices** onto the workspace canvas:

1. **Routers (Network Devices $\rightarrow$ Routers):**
   - Place **1x Cisco 2911** Router $\rightarrow$ Rename label to `R1_CORE_ROUTER`.
2. **Switches (Network Devices $\rightarrow$ Switches):**
   - Place **1x Cisco 2960-24TT** Switch $\rightarrow$ Rename label to `SW_CORE_01` (Center).
   - Place **1x Cisco 2960-24TT** Switch $\rightarrow$ Rename label to `SW_ACC_01` (Left).
   - Place **1x Cisco 2960-24TT** Switch $\rightarrow$ Rename label to `SW_ACC_02` (Right).
3. **Servers (End Devices $\rightarrow$ End Devices):**
   - Place **1x Server-PT** $\rightarrow$ Rename label to `SRV_BACKEND_01`.
   - Place **1x Server-PT** $\rightarrow$ Rename label to `SRV_FRONTEND_01`.
4. **IoT Energy Meters (End Devices $\rightarrow$ PC / IoT):**
   - Place **2x PC-PT** (or IoT Device) near `SW_ACC_01` $\rightarrow$ Rename labels to `LAB-01` and `LAB-02`.
   - Place **2x PC-PT** near `SW_ACC_01` $\rightarrow$ Rename labels to `CLASS-01` and `CLASS-02`.
   - Place **2x PC-PT** near `SW_ACC_02` $\rightarrow$ Rename labels to `LIB-01` and `ADMIN-01`.
5. **Workstations & Laptops (End Devices $\rightarrow$ End Devices):**
   - Place **1x PC-PT** near `SW_ACC_02` $\rightarrow$ Rename label to `PC_FACULTY_01`.
   - Place **1x Laptop-PT** near `SW_ACC_02` $\rightarrow$ Rename label to `PC_STUDENT_01`.

---

## PHASE B: Connect Cables

Select the **Connections** palette (Lightning bolt icon) and make the following connections:

### 1. Backbone Trunk Connections
- Select **Copper Straight-Through** (solid black line):
  - Connect `R1_CORE_ROUTER` port `GigabitEthernet0/0` to `SW_CORE_01` port `GigabitEthernet0/1`.
- Select **Copper Cross-Over** (dashed black line) or **Copper Straight-Through**:
  - Connect `SW_CORE_01` port `GigabitEthernet0/2` to `SW_ACC_01` port `GigabitEthernet0/1`.
  - Connect `SW_CORE_01` port `GigabitEthernet0/3` to `SW_ACC_02` port `GigabitEthernet0/1`.

### 2. Server Farm Connections (to `SW_CORE_01`)
- Select **Copper Straight-Through**:
  - Connect `SW_CORE_01` port `FastEthernet0/1` to `SRV_BACKEND_01` port `FastEthernet0`.
  - Connect `SW_CORE_01` port `FastEthernet0/2` to `SRV_FRONTEND_01` port `FastEthernet0`.

### 3. Access Switch 1 Connections (to `SW_ACC_01`)
- Select **Copper Straight-Through**:
  - Connect `SW_ACC_01` port `FastEthernet0/1` to `LAB-01` port `FastEthernet0`.
  - Connect `SW_ACC_01` port `FastEthernet0/2` to `LAB-02` port `FastEthernet0`.
  - Connect `SW_ACC_01` port `FastEthernet0/3` to `CLASS-01` port `FastEthernet0`.
  - Connect `SW_ACC_01` port `FastEthernet0/4` to `CLASS-02` port `FastEthernet0`.

### 4. Access Switch 2 Connections (to `SW_ACC_02`)
- Select **Copper Straight-Through**:
  - Connect `SW_ACC_02` port `FastEthernet0/1` to `LIB-01` port `FastEthernet0`.
  - Connect `SW_ACC_02` port `FastEthernet0/2` to `ADMIN-01` port `FastEthernet0`.
  - Connect `SW_ACC_02` port `FastEthernet0/3` to `PC_FACULTY_01` port `FastEthernet0`.
  - Connect `SW_ACC_02` port `FastEthernet0/4` to `PC_STUDENT_01` port `FastEthernet0`.

---

## PHASE C: Configure End-Device IP Addresses

For each end-device, click the device, navigate to the **Desktop** tab $\rightarrow$ click **IP Configuration** $\rightarrow$ select **Static**, and fill in the values:

| Device Name | IP Address | Subnet Mask | Default Gateway | DNS Server |
| :--- | :--- | :--- | :--- | :--- |
| `SRV_BACKEND_01` | `192.168.50.10` | `255.255.255.0` | `192.168.50.1` | `192.168.50.1` |
| `SRV_FRONTEND_01`| `192.168.50.20` | `255.255.255.0` | `192.168.50.1` | `192.168.50.1` |
| `LAB-01` | `192.168.10.10` | `255.255.255.0` | `192.168.10.1` | `192.168.50.1` |
| `LAB-02` | `192.168.10.11` | `255.255.255.0` | `192.168.10.1` | `192.168.50.1` |
| `CLASS-01` | `192.168.20.10` | `255.255.255.0` | `192.168.20.1` | `192.168.50.1` |
| `CLASS-02` | `192.168.20.11` | `255.255.255.0` | `192.168.20.1` | `192.168.50.1` |
| `LIB-01` | `192.168.30.10` | `255.255.255.0` | `192.168.30.1` | `192.168.50.1` |
| `ADMIN-01` | `192.168.30.20` | `255.255.255.0` | `192.168.30.1` | `192.168.50.1` |
| `PC_FACULTY_01` | `192.168.40.10` | `255.255.255.0` | `192.168.40.1` | `192.168.50.1` |
| `PC_STUDENT_01` | `192.168.40.11` | `255.255.255.0` | `192.168.40.1` | `192.168.50.1` |

---

## PHASE D: Configure Switch VLANs

### 1. `SW_CORE_01`
Click `SW_CORE_01` $\rightarrow$ **CLI** tab $\rightarrow$ press Enter $\rightarrow$ paste:

```cisco
enable
configure terminal
hostname SW_CORE_01
no ip domain-lookup

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

! Assign Server Farm Access Ports (VLAN 50)
interface range FastEthernet0/1 - 4
 description Server Farm Access Ports
 switchport mode access
 switchport access vlan 50
 spanning-tree portfast
 no shutdown
exit

! SVI Management Interface
interface Vlan99
 description Core Switch SVI Management
 ip address 192.168.99.2 255.255.255.0
 no shutdown
exit

ip default-gateway 192.168.99.1
exit
write memory
```

### 2. `SW_ACC_01` (Labs & Classrooms)
Click `SW_ACC_01` $\rightarrow$ **CLI** tab $\rightarrow$ press Enter $\rightarrow$ paste:

```cisco
enable
configure terminal
hostname SW_ACC_01
no ip domain-lookup

vlan 10
 name VLAN_LAB_IOT
vlan 20
 name VLAN_CLASS_IOT
vlan 99
 name VLAN_MANAGEMENT
exit

! Assign Lab Ports (VLAN 10)
interface range FastEthernet0/1 - 2
 description Computer Lab IoT Meters (LAB-01, LAB-02)
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
exit

! Assign Classroom Ports (VLAN 20)
interface range FastEthernet0/3 - 4
 description Classroom IoT Meters (CLASS-01, CLASS-02)
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 no shutdown
exit

! Security: Disable unused ports
interface range FastEthernet0/5 - 24, GigabitEthernet0/2
 shutdown
exit

! SVI Management Interface
interface Vlan99
 description SW_ACC_01 SVI Management
 ip address 192.168.99.11 255.255.255.0
 no shutdown
exit

ip default-gateway 192.168.99.1
exit
write memory
```

### 3. `SW_ACC_02` (Library, Admin & Users)
Click `SW_ACC_02` $\rightarrow$ **CLI** tab $\rightarrow$ press Enter $\rightarrow$ paste:

```cisco
enable
configure terminal
hostname SW_ACC_02
no ip domain-lookup

vlan 30
 name VLAN_LIB_ADMIN_IOT
vlan 40
 name VLAN_USERS
vlan 99
 name VLAN_MANAGEMENT
exit

! Assign Library & Admin Ports (VLAN 30)
interface range FastEthernet0/1 - 2
 description Library & Admin IoT Meters (LIB-01, ADMIN-01)
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 no shutdown
exit

! Assign User Ports (VLAN 40)
interface range FastEthernet0/3 - 12
 description User Workstations & Dashboard Clients
 switchport mode access
 switchport access vlan 40
 spanning-tree portfast
 no shutdown
exit

! Security: Disable unused ports
interface range FastEthernet0/13 - 24, GigabitEthernet0/2
 shutdown
exit

! SVI Management Interface
interface Vlan99
 description SW_ACC_02 SVI Management
 ip address 192.168.99.12 255.255.255.0
 no shutdown
exit

ip default-gateway 192.168.99.1
exit
write memory
```

---

## PHASE E: Configure Trunk Ports

### 1. `SW_CORE_01` Trunk Ports
On `SW_CORE_01` CLI:

```cisco
configure terminal

! Trunk Uplink to Router R1
interface GigabitEthernet0/1
 description Trunk to Router R1 Gig0/0
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
exit

! Trunk Downlink to SW_ACC_01
interface GigabitEthernet0/2
 description Trunk to SW_ACC_01 Gig0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,99
 no shutdown
exit

! Trunk Downlink to SW_ACC_02
interface GigabitEthernet0/3
 description Trunk to SW_ACC_02 Gig0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 30,40,99
 no shutdown
exit

exit
write memory
```

### 2. `SW_ACC_01` Trunk Port
On `SW_ACC_01` CLI:

```cisco
configure terminal
interface GigabitEthernet0/1
 description Uplink Trunk to SW_CORE_01 Gig0/2
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,99
 no shutdown
exit
exit
write memory
```

### 3. `SW_ACC_02` Trunk Port
On `SW_ACC_02` CLI:

```cisco
configure terminal
interface GigabitEthernet0/1
 description Uplink Trunk to SW_CORE_01 Gig0/3
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 30,40,99
 no shutdown
exit
exit
write memory
```

---

## PHASE F: Configure Router-on-a-Stick (ROAS) on `R1_CORE_ROUTER`

Click `R1_CORE_ROUTER` $\rightarrow$ **CLI** tab $\rightarrow$ type `no` if prompted for initial configuration dialog $\rightarrow$ paste:

```cisco
enable
configure terminal
hostname R1_CORE_ROUTER
no ip domain-lookup

! Bring up physical interface
interface GigabitEthernet0/0
 description Trunk Link to SW_CORE_01 Gig0/1
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

exit
write memory
```

---

## PHASE G: Configure Access Control Lists (ACLs)

> [!IMPORTANT]
> **Corrected Extended ACL Ordering Rule:**  
> Extended ACLs evaluate rules top-to-bottom on a first-match basis.  
> Lateral isolation `deny` rules are placed before generic telemetry/ICMP statements to ensure cross-VLAN probes between IoT devices and users are strictly blocked.

On `R1_CORE_ROUTER` CLI, execute:

```cisco
configure terminal

! =========================================================================
! ACL 10: LAB IoT SECURITY FILTER (VLAN 10 INBOUND)
! =========================================================================
ip access-list extended ACL_VLAN10_IN
 ! 1. Deny lateral cross-VLAN access to other IoT and User subnets FIRST
 deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255
 deny ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255
 deny ip 192.168.10.0 0.0.0.255 192.168.40.0 0.0.0.255
 ! 2. Permit REST API telemetry & HTTPS to Backend Server ONLY
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 8000
 permit tcp 192.168.10.0 0.0.0.255 host 192.168.50.10 eq 443
 ! 3. Permit ICMP to Default Gateway and Server Farm for diagnostics
 permit icmp 192.168.10.0 0.0.0.255 host 192.168.10.1
 permit icmp 192.168.10.0 0.0.0.255 192.168.50.0 0.0.0.255
 ! 4. Deny all other IP traffic
 deny ip any any
exit

! =========================================================================
! ACL 20: CLASSROOM IoT SECURITY FILTER (VLAN 20 INBOUND)
! =========================================================================
ip access-list extended ACL_VLAN20_IN
 ! 1. Deny lateral cross-VLAN access to other IoT and User subnets FIRST
 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255
 deny ip 192.168.20.0 0.0.0.255 192.168.30.0 0.0.0.255
 deny ip 192.168.20.0 0.0.0.255 192.168.40.0 0.0.0.255
 ! 2. Permit REST API telemetry & HTTPS to Backend Server ONLY
 permit tcp 192.168.20.0 0.0.0.255 host 192.168.50.10 eq 8000
 permit tcp 192.168.20.0 0.0.0.255 host 192.168.50.10 eq 443
 ! 3. Permit ICMP to Default Gateway and Server Farm for diagnostics
 permit icmp 192.168.20.0 0.0.0.255 host 192.168.20.1
 permit icmp 192.168.20.0 0.0.0.255 192.168.50.0 0.0.0.255
 ! 4. Deny all other IP traffic
 deny ip any any
exit

! =========================================================================
! ACL 30: LIB/ADMIN IoT SECURITY FILTER (VLAN 30 INBOUND)
! =========================================================================
ip access-list extended ACL_VLAN30_IN
 ! 1. Deny lateral cross-VLAN access to other IoT and User subnets FIRST
 deny ip 192.168.30.0 0.0.0.255 192.168.10.0 0.0.0.255
 deny ip 192.168.30.0 0.0.0.255 192.168.20.0 0.0.0.255
 deny ip 192.168.30.0 0.0.0.255 192.168.40.0 0.0.0.255
 ! 2. Permit REST API telemetry & HTTPS to Backend Server ONLY
 permit tcp 192.168.30.0 0.0.0.255 host 192.168.50.10 eq 8000
 permit tcp 192.168.30.0 0.0.0.255 host 192.168.50.10 eq 443
 ! 3. Permit ICMP to Default Gateway and Server Farm for diagnostics
 permit icmp 192.168.30.0 0.0.0.255 host 192.168.30.1
 permit icmp 192.168.30.0 0.0.0.255 192.168.50.0 0.0.0.255
 ! 4. Deny all other IP traffic
 deny ip any any
exit

! =========================================================================
! ACL 40: USERS SECURITY FILTER (VLAN 40 INBOUND)
! =========================================================================
ip access-list extended ACL_VLAN40_IN
 ! 1. Deny direct user access/probing into IoT meter VLANs FIRST
 deny ip 192.168.40.0 0.0.0.255 192.168.10.0 0.0.0.255
 deny ip 192.168.40.0 0.0.0.255 192.168.20.0 0.0.0.255
 deny ip 192.168.40.0 0.0.0.255 192.168.30.0 0.0.0.255
 ! 2. Permit Web Dashboard & FastAPI Backend Access
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.10 eq 8000
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.10 eq 443
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.20 eq 5173
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.20 eq 80
 permit tcp 192.168.40.0 0.0.0.255 host 192.168.50.20 eq 443
 ! 3. Permit ICMP to Gateway and Server Farm for diagnostics
 permit icmp 192.168.40.0 0.0.0.255 host 192.168.40.1
 permit icmp 192.168.40.0 0.0.0.255 192.168.50.0 0.0.0.255
 ! 4. Deny all other IP traffic
 deny ip any any
exit

! Bind ACLs to Router Sub-Interfaces
interface GigabitEthernet0/0.10
 ip access-group ACL_VLAN10_IN in
exit

interface GigabitEthernet0/0.20
 ip access-group ACL_VLAN20_IN in
exit

interface GigabitEthernet0/0.30
 ip access-group ACL_VLAN30_IN in
exit

interface GigabitEthernet0/0.40
 ip access-group ACL_VLAN40_IN in
exit

exit
write memory
```

---

## PHASE H: Verify Interfaces & Operational State

On `R1_CORE_ROUTER`, run:
```cisco
show ip interface brief
show interfaces trunk
show ip route
show access-lists
```

On `SW_CORE_01`, `SW_ACC_01`, and `SW_ACC_02`, run:
```cisco
show vlan brief
show interfaces trunk
```

Ensure all link lights turn **Green** in the Packet Tracer GUI. (Click **Fast Forward Time** if spanning tree ports are still amber).

---

## PHASE I: Run Connectivity Tests

1. **Test 1: IoT Meter to Default Gateway**
   - On `LAB-01` $\rightarrow$ Command Prompt:
     ```cmd
     ping 192.168.10.1
     ```
   - **Expected Result:** `Reply from 192.168.10.1: bytes=32 time<1ms TTL=255` (4/4 Success).

2. **Test 2: IoT Meter to Backend Server**
   - On `LAB-01` $\rightarrow$ Command Prompt:
     ```cmd
     ping 192.168.50.10
     ```
   - **Expected Result:** `Reply from 192.168.50.10: bytes=32 time<1ms TTL=127` (4/4 Success).

3. **Test 3: Faculty PC to Backend Server**
   - On `PC_FACULTY_01` $\rightarrow$ Command Prompt:
     ```cmd
     ping 192.168.50.10
     ```
   - **Expected Result:** `Reply from 192.168.50.10: bytes=32 time<1ms TTL=127` (4/4 Success).

4. **Test 4: Faculty PC to Web Dashboard Server**
   - On `PC_FACULTY_01` $\rightarrow$ Command Prompt:
     ```cmd
     ping 192.168.50.20
     ```
   - **Expected Result:** `Reply from 192.168.50.20: bytes=32 time<1ms TTL=127` (4/4 Success).

---

## PHASE J: Run ACL Security & Isolation Tests

1. **Test 5: Lateral IoT Isolation Test (`LAB-01` $\rightarrow$ `CLASS-01`)**
   - On `LAB-01` $\rightarrow$ Command Prompt:
     ```cmd
     ping 192.168.20.10
     ```
   - **Expected Result:** `Request timed out.` (Blocked by `ACL_VLAN10_IN` rule: `deny ip 192.168.10.0 0.0.0.255 192.168.20.0 0.0.0.255`).

2. **Test 6: Lateral IoT Isolation Test (`LAB-01` $\rightarrow$ `LIB-01`)**
   - On `LAB-01` $\rightarrow$ Command Prompt:
     ```cmd
     ping 192.168.30.10
     ```
   - **Expected Result:** `Request timed out.` (Blocked by `ACL_VLAN10_IN`).

3. **Test 7: IoT to User Workstation Isolation Test (`LAB-01` $\rightarrow$ `PC_FACULTY_01`)**
   - On `LAB-01` $\rightarrow$ Command Prompt:
     ```cmd
     ping 192.168.40.10
     ```
   - **Expected Result:** `Request timed out.` (Blocked by `ACL_VLAN10_IN`).

4. **Test 8: User to IoT Meter Isolation Test (`PC_FACULTY_01` $\rightarrow$ `LAB-01`)**
   - On `PC_FACULTY_01` $\rightarrow$ Command Prompt:
     ```cmd
     ping 192.168.10.10
     ```
   - **Expected Result:** `Request timed out.` (Blocked by `ACL_VLAN40_IN`).

5. **Test 9: Verify ACL Hit Counters on `R1_CORE_ROUTER`**
   - On `R1_CORE_ROUTER` CLI:
     ```cisco
     show access-lists
     ```
   - Verify that match counter increments are recorded against both permit and deny entries.

---

## PHASE K: Save the `.pkt` File

1. In Cisco Packet Tracer menu, click **File $\rightarrow$ Save As...**
2. Save the topology file as:
   `smart_campus_network.pkt`
3. Place the file inside the project directory at:
   `network/topology/smart_campus_network.pkt`
