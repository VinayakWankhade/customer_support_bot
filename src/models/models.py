"""
SQLAlchemy ORM models for database tables
"""
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey, CheckConstraint, Uuid, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class User(Base):
    """User profile table"""
    __tablename__ = "users"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    email = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Session(Base):
    """Support session table"""
    __tablename__ = "sessions"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    session_metadata = Column(JSON, default={})


class Message(Base):
    """Conversation message table"""
    __tablename__ = "messages"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(Uuid(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    role = Column(String(50), nullable=False)  # 'user' | 'assistant' | 'system'
    content = Column(Text, nullable=False)
    tokens = Column(Integer)
    confidence = Column(Float)
    sources = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class Escalation(Base):
    """Escalation ticket table"""
    __tablename__ = "escalations"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(Uuid(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    message_id = Column(Uuid(as_uuid=True), ForeignKey("messages.id"), nullable=True)
    severity = Column(String(50))  # 'low' | 'medium' | 'high' | 'critical'
    reason = Column(Text)
    ticket_ref = Column(String(100))
    status = Column(String(50), default="open")
    context_snapshot = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Feedback(Base):
    """User feedback table"""
    __tablename__ = "feedback"
    
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(Uuid(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    message_id = Column(Uuid(as_uuid=True), ForeignKey("messages.id"), nullable=True)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
