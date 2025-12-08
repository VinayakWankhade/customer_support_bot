"""
Integration tests for chat endpoint
(Mocks external LLM and Vector DB services)
"""
import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from src.services.llm_client import llm_client
from src.services.retriever import vector_db

@pytest.mark.asyncio
async def test_chat_happy_path(client):
    """Test standard chat flow with successful LLM response"""
    
    # 1. Create a session
    create_res = client.post("/session", json={})
    session_id = create_res.json()["session_id"]
    
    # 2. Mock LLM, Vector DB, and count_tokens
    mock_response_json = """
    {
        "answer_text": "To reset your password, visit the settings page.",
        "confidence": 0.9,
        "sources": ["faq_reset"],
        "next_action": "reply",
        "action_payload": {}
    }
    """
    
    with patch.object(llm_client, "generate_response", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = mock_response_json
        
        with patch.object(llm_client, "count_tokens", return_value=10):
            with patch.object(vector_db, "search", return_value=[{"text": "Reset password info...", "id": "faq_reset"}]):
                
                # 3. Send message
                payload = {
                    "session_id": session_id,
                    "message": "How do I reset my password?",
                    "stream": False
                }
                response = client.post("/chat", json=payload)
            
                # 4. Verify response
                assert response.status_code == 200
                data = response.json()
                assert data["answer_text"] == "To reset your password, visit the settings page."
                assert data["confidence"] == 0.9
                assert data["next_action"] == "reply"
                
                # Verify history
                hist_res = client.get(f"/session/{session_id}/history")
                msgs = hist_res.json()["messages"]
                assert len(msgs) == 2  # User msg + Assistant msg
                assert msgs[0]["role"] == "user"
                assert msgs[1]["role"] == "assistant"

@pytest.mark.asyncio
async def test_chat_session_not_found(client):
    """Test chat with invalid session ID"""
    payload = {
        "session_id": str(uuid4()),
        "message": "Hello"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_chat_llm_failure_handling(client):
    """Test handling of LLM failure/garbage output"""
    create_res = client.post("/session", json={})
    session_id = create_res.json()["session_id"]
    
    with patch.object(llm_client, "generate_response", new_callable=AsyncMock) as mock_llm:
        # LLM returns garbage string, not JSON
        mock_llm.return_value = "This is not JSON."
        
        with patch.object(llm_client, "count_tokens", return_value=5):
            payload = {"session_id": session_id, "message": "Hi"}
            response = client.post("/chat", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["answer_text"] == "This is not JSON."
            assert data["confidence"] == 0.5  # Fallback confidence
