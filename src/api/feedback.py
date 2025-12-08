"""
Feedback API Endpoint
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.database import get_db_dependency
from src.models.schemas import FeedbackCreate
from src.models.models import Feedback, Session as SessionModel, Message

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db_dependency)
):
    """
    Submit feedback for a specific message in a session
    """
    # 1. Validate Session
    session = db.query(SessionModel).filter(SessionModel.id == feedback_data.session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    # 2. Validate Message if provided
    if feedback_data.message_id:
        message = db.query(Message).filter(Message.id == feedback_data.message_id).first()
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        if message.session_id != feedback_data.session_id:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message does not belong to this session"
            )

    # 3. Save Feedback
    new_feedback = Feedback(
        session_id=feedback_data.session_id,
        message_id=feedback_data.message_id,
        rating=feedback_data.rating,
        comment=feedback_data.comment
    )
    
    db.add(new_feedback)
    db.commit()
    
    return {"status": "success", "message": "Feedback submitted"}
