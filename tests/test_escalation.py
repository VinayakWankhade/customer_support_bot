"""
Integration tests for escalation endpoint
"""
import pytest
from uuid import uuid4

def test_create_escalation_happy_path(client):
    """Test valid escalation creation"""
    # 1. Create Session
    session_res = client.post("/session", json={})
    session_id = session_res.json()["session_id"]
    
    # 2. Escalate
    payload = {
        "session_id": session_id,
        "reason": "billing_issue",
        "severity": "high"
    }
    response = client.post("/escalate", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "ticket_ref" in data
    assert data["ticket_ref"].startswith("TKT-")
    assert data["status"] == "open"
    assert "4 hours" in data["estimated_response_time"]

def test_escalation_invalid_severity(client):
    """Test escalation with invalid severity"""
    # 1. Create Session
    session_res = client.post("/session", json={})
    session_id = session_res.json()["session_id"]
    
    payload = {
        "session_id": session_id,
        "reason": "test",
        "severity": "super_critical" # Invalid enum
    }
    response = client.post("/escalate", json=payload)
    
    assert response.status_code == 422

def test_escalation_session_not_found(client):
    """Test escalation for non-existent session"""
    payload = {
        "session_id": str(uuid4()),
        "reason": "test",
        "severity": "low"
    }
    response = client.post("/escalate", json=payload)
    
    assert response.status_code == 404
