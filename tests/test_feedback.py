"""
Integration tests for feedback endpoint
"""
import pytest
from uuid import uuid4
from src.models.models import Message, Session
from uuid import UUID

def test_submit_feedback_happy_path(client, db_session):
    """Test valid feedback submission"""
    # 1. Create Session
    session_res = client.post("/session", json={})
    session_id = session_res.json()["session_id"]
    
    # 2. Create Message internally
    # Convert string uuid to UUID object
    session_uuid = UUID(session_id)
    
    msg = Message(session_id=session_uuid, role="assistant", content="Test", tokens=10)
    db_session.add(msg)
    db_session.commit()
    db_session.refresh(msg)
    msg_id = str(msg.id)
    
    # 3. Submit Feedback
    payload = {
        "session_id": session_id,
        "message_id": msg_id,
        "rating": 5,
        "comment": "Great!"
    }
    response = client.post("/feedback", json=payload)
    
    assert response.status_code == 201
    assert response.json()["status"] == "success"

def test_feedback_invalid_rating(client):
    """Test feedback with invalid rating"""
    payload = {
        "session_id": str(uuid4()),
        "message_id": str(uuid4()),
        "rating": 6, # Invalid
        "comment": "Too high"
    }
    response = client.post("/feedback", json=payload)
    assert response.status_code == 422 # Pydantic validation error

def test_feedback_session_not_found(client):
    """Test feedback for non-existent session"""
    payload = {
        "session_id": str(uuid4()),
        "message_id": str(uuid4()),
        "rating": 3
    }
    response = client.post("/feedback", json=payload)
    assert response.status_code == 404
