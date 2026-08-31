from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("\n--- 1. Testing GET /api/energy/summary ---")
response = client.get("/api/energy/summary")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\n--- 2. Testing POST /api/energy/readings (Valid Record) ---")
valid_record = {
    "device_id": "LAB-01",
    "area": "Computer Laboratory 1",
    "timestamp": "2026-08-23 10:00:00",
    "voltage": 230.5,
    "current": 10.2,
    "power": 2351.1,
    "energy": 0.5,
    "temperature": 25.4,
    "occupancy": 15
}
headers = {"X-API-Key": "iot_smart_energy_meter_key_2026_campus"}
response = client.post("/api/energy/readings", json=valid_record, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\n--- 3. Testing POST /api/energy/readings (Validation Error: Negative Power) ---")
invalid_record = valid_record.copy()
invalid_record["power"] = -100.0
response = client.post("/api/energy/readings", json=invalid_record, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\n--- 4. Testing GET /api/energy/readings ---")
response = client.get("/api/energy/readings?limit=2")
print(f"Status: {response.status_code}")
print(f"Retrieved records: {len(response.json())}")

print("\n--- 5. Checking /docs access ---")
response = client.get("/docs")
print(f"Status: {response.status_code} (OK indicates Swagger UI is working)")
