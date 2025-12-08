"""
Escalation Engine Service
"""
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Dict, Any, Optional
import random
from datetime import datetime, timedelta

from src.models.models import Escalation, Message
from src.models.schemas import EscalationCreate, EscalationResponse

class EscalationEngine:
    def __init__(self):
        pass

    def create_ticket(self, db: Session, data: EscalationCreate) -> EscalationResponse:
        """
        Create an escalation ticket
        """
        # Generate a ticket reference
        timestamp = datetime.now().strftime("%Y%m%d")
        rand_suffix = random.randint(1000, 9999)
        ticket_ref = f"TKT-{timestamp}-{rand_suffix}"
        
        # Build context snapshot
        context_snapshot = self._build_context_snapshot(db, data.session_id)
        
        # Create ticket
        new_ticket = Escalation(
            session_id=data.session_id,
            message_id=data.message_id,
            reason=data.reason,
            severity=data.severity,
            ticket_ref=ticket_ref,
            status="open",
            context_snapshot=context_snapshot
        )
        
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        
        # Calculate estimated response time based on severity
        sla_hours = {
            "low": 48,
            "medium": 24,
            "high": 4,
            "critical": 1
        }
        est_hours = sla_hours.get(data.severity, 24)
        
        return EscalationResponse(
            ticket_ref=new_ticket.ticket_ref,
            status=new_ticket.status,
            estimated_response_time=f"{est_hours} hours"
        )

    def _build_context_snapshot(self, db: Session, session_id: UUID) -> Dict[str, Any]:
        """
        Capture recent messages for ticket context
        """
        messages = db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(Message.timestamp.desc()).limit(5).all()
        
        return {
            "recent_messages": [
                {"role": m.role, "content": m.content, "timestamp": str(m.timestamp)} 
                for m in reversed(messages)
            ]
        }

escalation_engine = EscalationEngine()
