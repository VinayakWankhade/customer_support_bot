"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


# Session Schemas
class SessionCreate(BaseModel):
    """Request schema for creating a new session"""
    user_id: Optional[UUID] = None
    session_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, alias="metadata")


class SessionResponse(BaseModel):
    """Response schema for session creation"""
    session_id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SessionSummary(BaseModel):
    """Schema for session list summary"""
    id: UUID
    created_at: datetime
    last_active_at: datetime
    session_metadata: Dict[str, Any] = Field(default_factory=dict, serialization_alias="metadata")
    
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    """Response schema for a single message"""
    id: UUID
    role: str
    content: str
    confidence: Optional[float] = None
    sources: Optional[List[str]] = None
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SessionHistoryResponse(BaseModel):
    """Response schema for session history"""
    session_id: UUID
    created_at: datetime
    last_active_at: datetime
    messages: List[MessageResponse]
    
    model_config = ConfigDict(from_attributes=True)


# Chat Schemas
class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    session_id: UUID
    message: str
    stream: bool = False


class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    message_id: UUID
    answer_text: str
    confidence: float
    sources: List[str] = Field(default_factory=list)
    next_action: str = "reply"  # 'reply' | 'escalate' | 'create_ticket'
    action_payload: Dict[str, Any] = Field(default_factory=dict)


# Feedback Schemas
class FeedbackCreate(BaseModel):
    """Request schema for feedback submission"""
    session_id: UUID
    message_id: UUID
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


# Escalation Schemas
class EscalationCreate(BaseModel):
    """Request schema for escalation creation"""
    session_id: UUID
    message_id: Optional[UUID] = None
    reason: str
    severity: str = Field(pattern="^(low|medium|high|critical)$")


class EscalationResponse(BaseModel):
    """Response schema for escalation"""
    ticket_ref: str
    status: str
    estimated_response_time: str
    
    model_config = ConfigDict(from_attributes=True)
