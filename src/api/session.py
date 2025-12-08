"""
Session management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.database import get_db_dependency
from src.models.models import Session as SessionModel, Message, User
from src.models.schemas import (
    SessionCreate,
    SessionResponse,
    SessionHistoryResponse,
    MessageResponse
)

router = APIRouter(prefix="/session", tags=["Session"])


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db_dependency)
):
    """
    Create a new support session
    
    Args:
        session_data: Session creation data (optional user_id and metadata)
        db: Database session
        
    Returns:
        SessionResponse with session_id and created_at timestamp
    """
    # Validate user_id if provided
    if session_data.user_id:
        user = db.query(User).filter(User.id == session_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {session_data.user_id} not found"
            )
    
    # Create new session
    new_session = SessionModel(
        user_id=session_data.user_id,
        session_metadata=session_data.session_metadata or {}
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return SessionResponse(
        session_id=new_session.id,
        created_at=new_session.created_at
    )


@router.get("/{session_id}/history", response_model=SessionHistoryResponse)
async def get_session_history(
    session_id: UUID,
    db: Session = Depends(get_db_dependency)
):
    """
    Retrieve conversation history for a session
    
    Args:
        session_id: UUID of the session
        db: Database session
        
    Returns:
        SessionHistoryResponse with all messages in chronological order
    """
    # Fetch session
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    # Fetch all messages for this session
    messages = db.query(Message).filter(
        Message.session_id == session_id
    ).order_by(Message.timestamp.asc()).all()
    
    # Convert to response schema
    message_responses = [
        MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            confidence=msg.confidence,
            sources=msg.sources or [],
            timestamp=msg.timestamp
        )
        for msg in messages
    ]
    
    return SessionHistoryResponse(
        session_id=session.id,
        created_at=session.created_at,
        last_active_at=session.last_active_at,
        messages=message_responses
    )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def close_session(
    session_id: UUID,
    db: Session = Depends(get_db_dependency)
):
    """
    Close/delete a session
    
    Args:
        session_id: UUID of the session to close
        db: Database session
    """
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    db.delete(session)
    db.commit()
    
    return None
