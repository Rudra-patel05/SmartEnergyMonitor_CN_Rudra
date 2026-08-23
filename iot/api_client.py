import requests
from typing import List, Dict, Any

class ApiClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def send_reading(self, reading: Dict[str, Any]) -> bool:
        """Sends a single reading to the backend API."""
        url = f"{self.base_url}/api/energy/readings"
        try:
            response = requests.post(url, json=reading, timeout=5)
            if response.status_code == 201:
                return True
            elif response.status_code == 422:
                print(f"  [API ERROR 422] Validation failed: {response.text}")
                return False
            elif response.status_code >= 500:
                print(f"  [API ERROR {response.status_code}] Server error: {response.text}")
                return False
            else:
                print(f"  [API ERROR {response.status_code}] {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"  [CONNECTION ERROR] Failed to connect to {self.base_url}: {e}")
            return False

    def send_bulk_readings(self, readings: List[Dict[str, Any]]) -> bool:
        """Sends multiple readings to the backend API in bulk."""
        url = f"{self.base_url}/api/energy/readings/bulk"
        try:
            response = requests.post(url, json=readings, timeout=10)
            if response.status_code in (200, 201):
                return True
            elif response.status_code == 422:
                print(f"  [API ERROR 422] Validation failed: {response.text}")
                return False
            elif response.status_code >= 500:
                print(f"  [API ERROR {response.status_code}] Server error: {response.text}")
                return False
            else:
                print(f"  [API ERROR {response.status_code}] {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"  [CONNECTION ERROR] Failed to connect to {self.base_url}: {e}")
            return False
