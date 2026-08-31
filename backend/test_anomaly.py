import requests
import json

URL = "http://127.0.0.1:8000/api/anomaly/check"

# Controlled test payload representing an obvious abnormal energy condition (power spike)
payload = {
    "device_id": "LAB-TEST",
    "area": "Test Area",
    "timestamp": "2023-10-01 10:00:00",
    "voltage": 230.0,
    "current": 45.0, # Huge current for a simple lab test
    "power": 10350.0, # Massive power spike (230 * 45)
    "energy": 500.0,
    "temperature": 55.0, # Very high temp
    "occupancy": 0
}

print(f"Testing Anomaly Detection API at {URL}")
print("Sending test payload:")
print(json.dumps(payload, indent=2))

try:
    response = requests.post(URL, json=payload)
    print("\nStatus Code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", e)
