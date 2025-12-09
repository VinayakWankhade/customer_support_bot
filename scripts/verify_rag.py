import requests
import json
import time

BASE_URL = "http://localhost:8000"

questions = [
    "How do I reset my password?",
    "How can I update my billing information?",
    "What is your refund policy?",
    "Where can I find my API keys?",
    "How do I contact human support?"
]

# Create session first
session_res = requests.post(f"{BASE_URL}/session", json={})
session_id = session_res.json()["session_id"]
print(f"Created Session: {session_id}")

for q in questions:
    print(f"\nQuestion: {q}")
    payload = {"session_id": session_id, "message": q}
    try:
        res = requests.post(f"{BASE_URL}/chat", json=payload)
        res.raise_for_status()
        data = res.json()
        print(f"Answer: {data['answer_text']}")
        print(f"Confidence: {data['confidence']}")
        print(f"Sources: {data.get('sources', [])}")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1)
