import requests
import sys

try:
    # Target port 8002
    response = requests.get("http://localhost:8002/session")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
