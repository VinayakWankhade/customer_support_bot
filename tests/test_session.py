"""
Integration tests for session management endpoints
"""
import pytest
from uuid import uuid4
from src.models.models import User

def test_create_session_without_user(client):
    """Test creating a session without user_id"""
    response = client.post("/session", json={})
    
    assert response.status_code == 201
    data = response.json()
    assert "session_id" in data
    assert "created_at" in data

def test_create_session_with_user(client, db_session):
    """Test creating a session with valid user_id"""
    # Create user directly in DB
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    response = client.post(
        "/session",
        json={"user_id": str(user.id)}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "session_id" in data

def test_create_session_with_invalid_user(client):
    """Test creating a session with non-existent user_id"""
    fake_user_id = str(uuid4())
    response = client.post(
        "/session",
        json={"user_id": fake_user_id}
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_get_session_history(client):
    """Test retrieving session history"""
    # Create session
    create_response = client.post("/session", json={})
    session_id = create_response.json()["session_id"]
    
    # Get history
    response = client.get(f"/session/{session_id}/history")
    
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert "messages" in data
    assert isinstance(data["messages"], list)

def test_get_nonexistent_session_history(client):
    """Test retrieving history for non-existent session"""
    fake_session_id = str(uuid4())
    response = client.get(f"/session/{fake_session_id}/history")
    
    assert response.status_code == 404

def test_close_session(client):
    """Test closing/deleting a session"""
    # Create session
    create_response = client.post("/session", json={})
    session_id = create_response.json()["session_id"]
    
    # Close session
    response = client.delete(f"/session/{session_id}")
    
    assert response.status_code == 204
    
    # Verify session is deleted
    get_response = client.get(f"/session/{session_id}/history")
    assert get_response.status_code == 404
