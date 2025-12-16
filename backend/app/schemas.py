from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[int] = None
    # New Settings
    model_name: str = "gemini-1.5-flash"
    top_k: int = 4
    doc_filter: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: int
    citations: Optional[List[Any]] = None
    # New Context Return
    context: Optional[List[Dict[str, Any]]] = None

class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_hash: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class SessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    citations: Optional[List[Any]] = None
    
    class Config:
        from_attributes = True
