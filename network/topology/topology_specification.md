# 🗺️ Smart Campus Network Topology & Packet Tracer Specification

> **Project:** AI-Driven Smart Energy Consumption Monitoring & Prediction System for Smart Campus  
> **Module:** Network Architecture & Computer Networks (Day 11)  
> **Target Simulator:** Cisco Packet Tracer 8.x+ / GNS3 / Physical Lab

---

## 1. Network Topology Diagram (Mermaid)

```mermaid
graph TD
    subgraph "Core Routing Layer"
        R1["Router R1 (Cisco 2911)<br/>Router-on-a-Stick<br/>Gig0/0.10: 192.168.10.1<br/>Gig0/0.20: 192.168.20.1<br/>Gig0/0.30: 192.168.30.1<br/>Gig0/0.40: 192.168.40.1<br/>Gig0/0.50: 192.168.50.1"]
    end

    subgraph "Distribution / Core Switching Layer"
        SW_CORE["Core Switch SW-CORE-01<br/>Cisco Catalyst 2960<br/>VLAN 99 SVI: 192.168.99.2"]
    end

    subgraph "Server Farm (VLAN 50)"
        SRV_API["FastAPI Backend & ML<br/>IP: 192.168.50.10"]
        SRV_WEB["Web Dashboard<br/>IP: 192.168.50.20"]
    end

    subgraph "Access Layer — Labs & Classrooms"
        SW_ACC1["Access Switch SW-ACC-01<br/>VLAN 10 & VLAN 20"]
        IOT_LAB1["LAB-01 Meter<br/>192.168.10.10"]
        IOT_LAB2["LAB-02 Meter<br/>192.168.10.11"]
        IOT_CLS1["CLASS-01 Meter<br/>192.168.20.10"]
        IOT_CLS2["CLASS-02 Meter<br/>192.168.20.11"]
    end

    subgraph "Access Layer — Library, Admin & Users"
        SW_ACC2["Access Switch SW-ACC-02<br/>VLAN 30 & VLAN 40"]
        IOT_LIB["LIB-01 Meter<br/>192.168.30.10"]
        IOT_ADM["ADMIN-01 Meter<br/>192.168.30.20"]
        PC_USER1["Faculty PC<br/>192.168.40.10"]
        PC_USER2["Student Laptop<br/>192.168.40.11"]
    end

    %% Connections
    R1 <== "802.1Q Trunk (Gig0/0 <-> Gig0/1)" ==> SW_CORE
    SW_CORE <== "Trunk (Gig0/2 <-> Gig0/1)" ==> SW_ACC1
    SW_CORE <== "Trunk (Gig0/3 <-> Gig0/1)" ==> SW_ACC2
    SW_CORE --- "Fa0/1 (VLAN 50)" --- SRV_API
    SW_CORE --- "Fa0/2 (VLAN 50)" --- SRV_WEB

    SW_ACC1 --- "Fa0/1 (VLAN 10)" --- IOT_LAB1
    SW_ACC1 --- "Fa0/2 (VLAN 10)" --- IOT_LAB2
    SW_ACC1 --- "Fa0/3 (VLAN 20)" --- IOT_CLS1
    SW_ACC1 --- "Fa0/4 (VLAN 20)" --- IOT_CLS2

    SW_ACC2 --- "Fa0/1 (VLAN 30)" --- IOT_LIB
    SW_ACC2 --- "Fa0/2 (VLAN 30)" --- IOT_ADM
    SW_ACC2 --- "Fa0/3 (VLAN 40)" --- PC_USER1
    SW_ACC2 --- "Fa0/4 (VLAN 40)" --- PC_USER2
```

---

## 2. Cisco Packet Tracer Setup Instructions (Step-by-Step)

If building this topology in Cisco Packet Tracer:

1. **Place Devices in Workspace:**
   - **1x Cisco 2911 Router** $\rightarrow$ Label as `R1_CORE_ROUTER`.
   - **3x Cisco 2960-24TT Switches** $\rightarrow$ Label as `SW_CORE_01`, `SW_ACC_01`, `SW_ACC_02`.
   - **2x Server-PT** $\rightarrow$ Label as `SRV_BACKEND_01` and `SRV_FRONTEND_01`.
   - **6x Generic IoT Devices / Generic PCs** $\rightarrow$ Label as `LAB-01`, `LAB-02`, `CLASS-01`, `CLASS-02`, `LIB-01`, `ADMIN-01`.
   - **2x Generic PC / Laptop** $\rightarrow$ Label as `PC_FACULTY_01`, `PC_STUDENT_01`.

2. **Cabling Instructions:**
   - Connect `R1 Gig0/0` to `SW_CORE_01 Gig0/1` using a Copper Straight-Through cable.
   - Connect `SW_CORE_01 Gig0/2` to `SW_ACC_01 Gig0/1` using Copper Straight-Through.
   - Connect `SW_CORE_01 Gig0/3` to `SW_ACC_02 Gig0/1` using Copper Straight-Through.
   - Connect Server ports to `SW_CORE_01 Fa0/1` and `Fa0/2`.
   - Connect Lab IoT meters to `SW_ACC_01 Fa0/1` and `Fa0/2`.
   - Connect Classroom IoT meters to `SW_ACC_01 Fa0/3` and `Fa0/4`.
   - Connect Library/Admin IoT meters to `SW_ACC_02 Fa0/1` and `Fa0/2`.
   - Connect User PCs to `SW_ACC_02 Fa0/3` and `Fa0/4`.

3. **Apply Configurations:**
   - Open CLI tab on each device and paste the corresponding script from `network/topology/cisco_ios_configs.md`.

4. **Verify Connectivity in Packet Tracer:**
   - From `LAB-01` (`192.168.10.10`), ping default gateway: `ping 192.168.10.1` (Result: 4/4 Success).
   - From `LAB-01`, ping backend server: `ping 192.168.50.10` (Result: 4/4 Success).
   - From `LAB-01`, attempt to ping classroom IoT meter: `ping 192.168.20.10` (Result: Blocked by ACL).
   - From `PC_FACULTY_01` (`192.168.40.10`), ping backend server: `ping 192.168.50.10` (Result: 4/4 Success).
