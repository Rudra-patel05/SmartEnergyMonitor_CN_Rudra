import time
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"
ANOMALY_URL = f"{BASE_URL}/api/anomaly/check"
API_KEY = "iot_smart_energy_meter_key_2026_campus"
HEADERS = {"X-API-Key": API_KEY}

def run_integration_tests():
    print("=" * 70)
    print("[*] STARTING COMPLETE SYSTEM INTEGRATION & END-TO-END VERIFICATION")
    print("=" * 70)
    
    # 1. API Health & Summary
    print("\n[STEP 1] Verifying Backend API Health & Summaries:")
    start_time = time.time()
    try:
        resp = requests.get(f"{BASE_URL}/api/energy/summary")
        latency = (time.time() - start_time) * 1000
        print(f"  - GET /api/energy/summary: Status {resp.status_code} ({latency:.1f}ms)")
        assert resp.status_code == 200, "Summary endpoint failed!"
        summary = resp.json()
        print(f"  - Total Stored Readings: {summary['total_readings']}")
        print(f"  - System Average Power: {summary['average_power']} W")
    except Exception as e:
        print(f"  [FAIL] Step 1 Failed: {e}")
        return False
        
    # 2. IoT Data Ingestion (Telemetry Ingestion)
    print("\n[STEP 2] Simulating Authenticated Telemetry Ingestion from IoT Meter:")
    reading = {
        "device_id": "LAB-01",
        "area": "Computer Laboratory 1",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "voltage": 230.0,
        "current": 1.3,
        "power": 299.0,
        "energy": 2.5000,
        "temperature": 23.5,
        "occupancy": 15
    }
    start_time = time.time()
    try:
        resp = requests.post(f"{BASE_URL}/api/energy/readings", json=reading, headers=HEADERS)
        latency = (time.time() - start_time) * 1000
        print(f"  - POST /api/energy/readings: Status {resp.status_code} ({latency:.1f}ms)")
        assert resp.status_code == 201, "Ingestion failed!"
        print(f"  - Successfully stored reading ID: {resp.json().get('id')}")
    except Exception as e:
        print(f"  [FAIL] Step 2 Failed: {e}")
        return False
        
    # 3. Database Persistent Verification
    print("\n[STEP 3] Verifying Telemetry Persistence in SQLite Database:")
    start_time = time.time()
    try:
        resp = requests.get(f"{BASE_URL}/api/energy/readings?device_id=LAB-01&limit=5")
        latency = (time.time() - start_time) * 1000
        print(f"  - GET /api/energy/readings?device_id=LAB-01: Status {resp.status_code} ({latency:.1f}ms)")
        assert resp.status_code == 200, "Query readings failed!"
        data = resp.json()
        assert len(data) > 0, "No readings returned!"
        print(f"  - Latest reading retrieved from DB: ID {data[0]['id']} at timestamp {data[0]['timestamp']}")
    except Exception as e:
        print(f"  [FAIL] Step 3 Failed: {e}")
        return False

    # 4. XGBoost Prediction Verification
    print("\n[STEP 4] Requesting XGBoost Energy Consumption Forecasting:")
    payload = {"device_id": "LAB-01"}
    start_time = time.time()
    try:
        # Step 4 needs user authentication, but wait! Let's login first to get a token.
        login_credentials = {"username": "operator", "password": "Operator@123!"}
        login_resp = requests.post(f"{BASE_URL}/api/auth/token", json=login_credentials)
        token = login_resp.json()["access_token"]
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        resp = requests.post(f"{BASE_URL}/api/prediction/energy/predict", json=payload, headers=auth_headers)
        latency = (time.time() - start_time) * 1000
        print(f"  - POST /api/prediction/energy/predict: Status {resp.status_code} ({latency:.1f}ms)")
        assert resp.status_code == 200, "Forecasting endpoint failed!"
        pred = resp.json()
        print(f"  - Predicted Next Energy: {pred['predicted_next_energy']:.4f} kWh")
        print(f"  - Model Used: {pred['model_name']}")
    except Exception as e:
        print(f"  [FAIL] Step 4 Failed: {e}")
        return False

    # 5. Isolation Forest Anomaly Detection Verification
    print("\n[STEP 5] Testing Isolation Forest Anomaly Engine:")
    try:
        # Test Latest Anomaly Status across devices
        start_time = time.time()
        resp_lat = requests.get(f"{BASE_URL}/api/anomaly/latest")
        lat_lat = (time.time() - start_time) * 1000
        print(f"  - GET /api/anomaly/latest: Status {resp_lat.status_code} ({lat_lat:.1f}ms)")
        assert resp_lat.status_code == 200, "GET latest anomalies failed!"
        device_anomalies = resp_lat.json()
        print(f"    - Devices evaluated: {len(device_anomalies)}")
        for d in device_anomalies:
            print(f"    - Device {d['device_id']}: Flag {d['anomaly_flag']} | Score {d['anomaly_score']:.4f} | Status {d['status']}")
        
        # Test Normal Telemetry Check using the latest valid reading from DB
        db_reading = requests.get(f"{BASE_URL}/api/energy/readings?device_id=LAB-01&limit=1").json()[0]
        normal_payload = {
            "device_id": db_reading["device_id"],
            "area": db_reading["area"],
            "timestamp": db_reading["timestamp"],
            "voltage": db_reading["voltage"],
            "current": db_reading["current"],
            "power": db_reading["power"],
            "energy": db_reading["energy"],
            "temperature": db_reading["temperature"],
            "occupancy": db_reading["occupancy"]
        }
        start_time = time.time()
        resp_norm = requests.post(ANOMALY_URL, json=normal_payload, headers=auth_headers)
        lat_norm = (time.time() - start_time) * 1000
        print(f"  - POST /api/anomaly/check (Normal DB Reading): Status {resp_norm.status_code} ({lat_norm:.1f}ms)")
        assert resp_norm.status_code == 200, "Check normal anomaly failed!"
        norm_res = resp_norm.json()
        print(f"    - Flag: {norm_res['anomaly_flag']} | Score: {norm_res['anomaly_score']:.4f} | Status: {norm_res['status']}")
        
        # Test Anomaly Telemetry
        abnormal_payload = {
            "device_id": "LAB-01",
            "area": "Computer Laboratory 1",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "voltage": 230.0,
            "current": 48.0,      # Extreme current draw
            "power": 11040.0,     # Massive power spike
            "energy": 2.5000,
            "temperature": 58.5,  # High temperature
            "occupancy": 0        # Unoccupied area
        }
        start_time = time.time()
        resp_abn = requests.post(ANOMALY_URL, json=abnormal_payload, headers=auth_headers)
        lat_abn = (time.time() - start_time) * 1000
        print(f"  - POST /api/anomaly/check (Abnormal): Status {resp_abn.status_code} ({lat_abn:.1f}ms)")
        assert resp_abn.status_code == 200, "Check abnormal anomaly failed!"
        abn_res = resp_abn.json()
        print(f"    - Flag: {abn_res['anomaly_flag']} | Score: {abn_res['anomaly_score']:.4f} | Status: {abn_res['status']}")
        assert abn_res["status"] == "ANOMALY", "Failed to flag obvious anomaly!"
        
        # Test Latest Anomaly Status SVI
        start_time = time.time()
        resp_lat = requests.get(f"{BASE_URL}/api/anomaly/latest")
        lat_lat = (time.time() - start_time) * 1000
        print(f"  - GET /api/anomaly/latest: Status {resp_lat.status_code} ({lat_lat:.1f}ms)")
        assert resp_lat.status_code == 200, "GET latest anomalies failed!"
        print(f"    - Devices evaluated: {len(resp_lat.json())}")
        
    except Exception as e:
        print(f"  [FAIL] Step 5 Failed: {e}")
        return False
        
    print("\n" + "=" * 70)
    print("[SUCCESS] ALL END-TO-END INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    if not run_integration_tests():
        sys.exit(1)
