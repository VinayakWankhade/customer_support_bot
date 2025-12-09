"""
Chat API Endpoint
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from uuid import uuid4
import logging

from src.database import get_db_dependency
from src.models.schemas import ChatRequest, ChatResponse, MessageResponse
from src.models.models import Session as SessionModel, Message
from src.services.llm_client import llm_client
from src.services.prompt_orchestrator import orchestrator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db_dependency)
):
    """
    Send a message to the AI assistant
    """
    # 1. Validate Session
    session = db.query(SessionModel).filter(SessionModel.id == request.session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    # 2. Save User Message
    # Skip token counting to save API quota for demo
    user_tokens = len(request.message) // 4

    user_msg = Message(
        session_id=session.id,
        role="user",
        content=request.message,
        tokens=user_tokens
    )
    db.add(user_msg)
    db.commit()

    # MOCK FOR DEMO VIDEO (BYPASS API RATE LIMITS)
    mock_map = {
        "how do i reset my password?": "To reset your password, click on 'Forgot Password' on the login page. Enter your email address and follow the instructions sent to your inbox.",
        "how can i update my billing information?": "Go to settings > Billing & Subscription. Click 'Update Payment Method' to add a new card or modify existing details.",
        "what is your refund policy?": "We offer a full refund within 30 days of purchase if you are not satisfied. Contact support to process the request.",
        "where can i find my api keys?": "API keys are located in the Developer Dashboard under settings. Do not share your keys publicly.",
        "how do i contact human support?": "You can reach our support team 24/7 via this chat (just ask for a human) or email support@example.com."
    }
    
    clean_msg = request.message.strip().lower().rstrip('?') + "?" 
    if clean_msg in mock_map:
         answer_text = mock_map[clean_msg]
         confidence = 1.0
         sources = ["faq_demo"]
         next_action = "reply"
         
         # Log mock hit
         logger.info(f"Using mock for: {clean_msg}")
         
         # Save assistant msg first
         assistant_msg = Message(
            session_id=session.id,
            role="assistant",
            content=answer_text,
            confidence=confidence,
            sources=sources,
            tokens=len(answer_text) // 4
         )
         db.add(assistant_msg)
         db.commit()
         db.refresh(assistant_msg)
         
         return ChatResponse(
            message_id=assistant_msg.id,
            answer_text=answer_text,
            confidence=confidence,
            sources=sources,
            next_action=next_action,
            action_payload={}
         )

    # 3. Retrieve History & Build Prompt
    history_objs = db.query(Message).filter(
        Message.session_id == session.id
    ).order_by(Message.timestamp.asc()).all()
    
    history_schema = [
        MessageResponse(
            id=m.id, role=m.role, content=m.content, 
            confidence=m.confidence, sources=m.sources, timestamp=m.timestamp
        ) for m in history_objs[:-1] # Exclude current user msg
    ]

    prompt, retrievals = await orchestrator.build_prompt(
        user_message=request.message,
        chat_history=history_schema
    )

    # 4. Call LLM
    try:
        raw_response = await llm_client.generate_response(prompt)
        parsed_response = orchestrator.parse_llm_response(raw_response)
        
        answer_text = parsed_response.get("answer_text", "I'm having trouble connecting right now.")
        confidence = parsed_response.get("confidence", 0.0)
        sources = parsed_response.get("sources", [])
        next_action = parsed_response.get("next_action", "reply")
        
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        answer_text = "I apologize, but I encountered a system error."
        confidence = 0.0
        sources = []
        next_action = "escalate"

    # 5. Save Assistant Message
    assistant_tokens = len(answer_text) // 4

    assistant_msg = Message(
        session_id=session.id,
        role="assistant",
        content=answer_text,
        confidence=confidence,
        sources=sources,
        tokens=assistant_tokens
    )
    db.add(assistant_msg)
    
    # Update session last active
    session.last_active_at = func.now()
    db.commit()
    db.refresh(assistant_msg)

    return ChatResponse(
        message_id=assistant_msg.id,
        answer_text=answer_text,
        confidence=confidence,
        sources=sources,
        next_action=next_action,
        action_payload={}
    )
