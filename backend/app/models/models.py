from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.session import Base


class User(Base):
    """User accounts table."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Session(Base):
    """Chat sessions table."""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), default="New Chat", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Document(Base):
    """Uploaded PDF documents table."""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(500), nullable=False)
    file_hash = Column(String(64), unique=True, nullable=False, index=True)
    status = Column(String(50), default="indexing", nullable=False)  # indexing, indexed, error
    num_pages = Column(Integer)
    num_chunks = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Message(Base):
    """Chat messages table with citations."""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    citations = Column(JSON)  # [{doc, page, content}, ...]
    context = Column(JSON)  # Full retrieved chunks
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Metric(Base):
    """Query performance metrics table."""
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    query = Column(Text, nullable=False)
    latency_ms = Column(Integer)
    chunks_retrieved = Column(Integer)
    model_used = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
