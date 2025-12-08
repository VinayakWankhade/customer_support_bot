"""
Escalation API Endpoint
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.database import get_db_dependency
from src.models.schemas import EscalationCreate, EscalationResponse
from src.models.models import Session as SessionModel
from src.services.escalation_engine import escalation_engine

router = APIRouter(prefix="/escalate", tags=["Escalation"])

@router.post("", response_model=EscalationResponse, status_code=status.HTTP_201_CREATED)
async def create_escalation(
    escalation_data: EscalationCreate,
    db: Session = Depends(get_db_dependency)
):
    """
    Create an escalation ticket
    """
    # Validate session
    session = db.query(SessionModel).filter(SessionModel.id == escalation_data.session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
        
    return escalation_engine.create_ticket(db, escalation_data)
